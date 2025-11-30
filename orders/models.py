from django.db import models
from django.contrib.auth.models import User
from menu.models import MenuItem

# Stores a single completed order
class Order(models.Model):
    PAYMENT_CHOICES = [
        ("BANK", "Bank Transfer"),
        ("CASH", "Cash on Pickup"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="Pending")  # Pending / Completed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


# Items inside an order (copied from cart on checkout)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantity * self.price_at_purchase


# Bank payment details
class BankPaymentDetails(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="bank_details")
    phone_used = models.CharField(max_length=20)
    note = models.TextField(blank=True)  # Optional

    def __str__(self):
        return f"Bank Payment for Order #{self.order.id}"


# Cash on pickup
class CashPickupDetails(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="cash_details")
    pickup_name = models.CharField(max_length=100)
    pickup_phone = models.CharField(max_length=20)

    def __str__(self):
        return f"Cash Pickup for Order #{self.order.id}"
