from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cart.models import CartItem
from deals.models import Deal
from menu.models import MenuItem
from .models import Order, OrderItem, BankPaymentDetails, CashPickupDetails
from .serializers import OrderSerializer


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.subtotal() for item in cart_items)

    return render(request, "orders/checkout.html", {
        "cart_items": cart_items,
        "total": total,
        "user_email": request.user.email,
    })


@login_required
def place_order(request):
    if request.method != "POST":
        return redirect("orders:checkout")

    payment_method = request.POST.get("payment_method")
    email = request.POST.get("email")

    # Read the optional location values submitted by the checkout page.
    latitude = request.POST.get("latitude")
    longitude = request.POST.get("longitude")
    distance_from_kafei = request.POST.get("distance_from_kafei")

    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.subtotal() for item in cart_items)

    order = Order.objects.create(
        user=request.user,
        email=email,
        payment_method=payment_method,
        total_price=total_price,
        latitude=latitude if latitude else None,
        longitude=longitude if longitude else None,
        distance_from_kafei=distance_from_kafei if distance_from_kafei else None,
    )

    for item in cart_items:
        if item.item_type == "MENU":
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price_at_purchase=item.product.price
            )
        elif item.item_type == "DEAL":
            OrderItem.objects.create(
                order=order,
                deal=item.deal,
                quantity=item.quantity,
                price_at_purchase=item.deal.price_after
            )

    if payment_method == "BANK":
        BankPaymentDetails.objects.create(
            order=order,
            phone_used=request.POST.get("bank_phone"),
            note=request.POST.get("bank_note")
        )
    else:
        CashPickupDetails.objects.create(
            order=order,
            pickup_name=request.POST.get("pickup_name"),
            pickup_phone=request.POST.get("pickup_phone")
        )

    cart_items.delete()

    return redirect("orders:success")


@login_required
def success(request):
    return render(request, "orders/success.html")


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "orders/order_history.html", {"orders": orders})


@login_required
def order_now_deal(request, deal_id):
    deal = get_object_or_404(Deal, id=deal_id)

    CartItem.objects.create(
        user=request.user,
        deal=deal,
        item_type="DEAL",
        quantity=1
    )

    return redirect("orders:checkout")


class OrderListAPI(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


def create_order_item_from_payload(order, item_data):
    # Convert one API cart item into a saved OrderItem row.
    item_type = item_data.get("item_type", "MENU")
    item_id = item_data.get("item_id") or item_data.get("id")
    quantity = int(item_data.get("quantity", 1))

    if quantity < 1:
        quantity = 1

    if item_type == "MENU":
        product = get_object_or_404(MenuItem, id=item_id, is_active=True)
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price_at_purchase=product.price,
        )
        return product.price * quantity

    if item_type == "DEAL":
        deal = get_object_or_404(Deal, id=item_id, is_active=True)
        OrderItem.objects.create(
            order=order,
            deal=deal,
            quantity=quantity,
            price_at_purchase=deal.price_after,
        )
        return deal.price_after * quantity

    raise ValueError("Invalid item type")


def create_order_item_from_cart(order, cart_item):
    if cart_item.item_type == "MENU" and cart_item.product:
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price_at_purchase=cart_item.product.price,
        )
        return cart_item.product.price * cart_item.quantity

    if cart_item.item_type == "DEAL" and cart_item.deal:
        OrderItem.objects.create(
            order=order,
            deal=cart_item.deal,
            quantity=cart_item.quantity,
            price_at_purchase=cart_item.deal.price_after,
        )
        return cart_item.deal.price_after * cart_item.quantity

    return Decimal("0.00")


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def place_order_api(request):
    # Authenticated mobile/API clients send cart items and optional location values here.
    payment_method = request.data.get("payment_method", "CASH")
    email = request.data.get("email") or request.user.email
    items = request.data.get("items", [])

    if payment_method not in ["BANK", "CASH"]:
        return Response({"error": "payment_method must be BANK or CASH"}, status=400)

    order = Order.objects.create(
        user=request.user,
        email=email,
        payment_method=payment_method,
        total_price=Decimal("0.00"),
        latitude=request.data.get("latitude"),
        longitude=request.data.get("longitude"),
        distance_from_kafei=request.data.get("distance_from_kafei"),
    )

    total_price = Decimal("0.00")

    try:
        if items:
            for item_data in items:
                total_price += create_order_item_from_payload(order, item_data)
        else:
            cart_items = CartItem.objects.filter(user=request.user)

            if not cart_items.exists():
                order.delete()
                return Response({"error": "Cart is empty"}, status=400)

            for cart_item in cart_items:
                total_price += create_order_item_from_cart(order, cart_item)

            cart_items.delete()

    except ValueError as error:
        order.delete()
        return Response({"error": str(error)}, status=400)

    order.total_price = total_price
    order.save()

    if payment_method == "BANK":
        BankPaymentDetails.objects.create(
            order=order,
            phone_used=request.data.get("bank_phone", ""),
            note=request.data.get("bank_note", ""),
        )
    else:
        CashPickupDetails.objects.create(
            order=order,
            pickup_name=request.data.get("pickup_name") or request.user.username,
            pickup_phone=request.data.get("pickup_phone", ""),
        )

    serializer = OrderSerializer(order)
    return Response(serializer.data, status=201)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def latest_order_api(request):
    order = Order.objects.filter(user=request.user).order_by("-created_at").first()

    if order is None:
        return Response({"error": "No orders found"}, status=404)

    serializer = OrderSerializer(order)
    return Response(serializer.data)
