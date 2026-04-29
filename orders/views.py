from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import CartItem
from deals.models import Deal
from .models import Order, OrderItem, BankPaymentDetails, CashPickupDetails
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Order
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

    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.subtotal() for item in cart_items)

    # Create order
    order = Order.objects.create(
        user=request.user,
        email=email,
        payment_method=payment_method,
        total_price=total_price,
    )

    # Create order items for both menu items and deals
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

    # Save payment details
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

    
    CartItem.objects.filter(user=request.user, temp_order_now=True).delete()

  
    CartItem.objects.create(
        user=request.user,
        deal=deal,
        item_type="DEAL",
        quantity=1,
        temp_order_now=True
    )


    return redirect("orders:checkout")





class OrderListAPI(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')