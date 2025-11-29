from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import CartItem
from .models import Order, OrderItem, BankPaymentDetails, CashPickupDetails

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

    # Create order items
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price_at_purchase=item.product.price
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

    # Clear cart
    cart_items.delete()

    return redirect("orders:success")


@login_required
def success(request):
    return render(request, "orders/success.html")
