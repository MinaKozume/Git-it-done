from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import random

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from menu.models import MenuItem
from deals.models import Deal
from .models import CartItem
from .serializers import CartItemSerializer


# -------------------------
# ADD MENU ITEM TO CART
# -------------------------
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(MenuItem, id=product_id)

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            item_type='MENU',
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})

        return redirect(request.META.get("HTTP_REFERER", "cart:view_cart"))

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

    return redirect("cart:view_cart")


# -------------------------
# ADD DEAL TO CART
# -------------------------
@login_required
def add_deal_to_cart(request, deal_id):
    deal = get_object_or_404(Deal, id=deal_id)

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            deal=deal,
            item_type='DEAL',
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": True})

        return redirect(request.META.get("HTTP_REFERER", "cart:view_cart"))

    return redirect("deals:deals")


# -------------------------
# VIEW CART
# -------------------------
@login_required
def view_cart(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.subtotal() for item in items)

    cart_product_ids = items.values_list("product_id", flat=True)
    suggestions = list(MenuItem.objects.filter(is_active=True).exclude(id__in=cart_product_ids))
    random.shuffle(suggestions)
    suggestions = suggestions[:4]

    return render(request, "cart/cart.html", {
        "items": items,
        "total": total,
        "suggestions": suggestions
    })


# -------------------------
# UPDATE QUANTITY
# -------------------------
@login_required
def update_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    new_qty = int(request.POST.get("quantity"))

    if new_qty > 0:
        item.quantity = new_qty
        item.save()

    return redirect("cart:view_cart")


# -------------------------
# REMOVE ITEM
# -------------------------
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect("cart:view_cart")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart_list_api(request):
    cart_items = CartItem.objects.filter(user=request.user)
    serializer = CartItemSerializer(cart_items, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart_api(request):
    item_type = request.data.get("item_type")
    item_id = request.data.get("item_id")
    quantity = int(request.data.get("quantity", 1))

    if item_type == "MENU":
        product = get_object_or_404(MenuItem, id=item_id)
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            item_type="MENU",
            defaults={"quantity": quantity}
        )

    elif item_type == "DEAL":
        deal = get_object_or_404(Deal, id=item_id)
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            deal=deal,
            item_type="DEAL",
            defaults={"quantity": quantity}
        )

    else:
        return Response({"error": "Invalid item type"}, status=400)

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return Response({"message": "Item added to cart"})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart_api(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return Response({"message": "Item removed"})
