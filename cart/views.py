from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from menu.models import MenuItem
from .models import CartItem

# ADD TO CART
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(MenuItem, id=product_id)

    # print("ADD TO CART CALLED!", product_id) -for debug

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )

    # If item already in cart → increase quantity
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart:view_cart")


# VIEW CART
@login_required
def view_cart(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.subtotal() for item in items)

    return render(request, "cart/cart.html", {
        "items": items,
        "total": total
    })


# UPDATE QUANTITY
@login_required
def update_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    new_qty = int(request.POST.get("quantity"))

    if new_qty > 0:
        item.quantity = new_qty
        item.save()

    return redirect("cart:view_cart")


# REMOVE ITEM
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect("cart:view_cart")
