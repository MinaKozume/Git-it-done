from django.db import models
from django.contrib.auth.models import User
from menu.models import MenuItem
from deals.models import Deal


class Order(models.Model):
    PAYMENT_CHOICES = [
        ("BANK", "Bank Transfer"),
        ("CASH", "Cash on Pickup"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("completed", "Completed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )    
    created_at = models.DateTimeField(auto_now_add=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    distance_from_kafei = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True, blank=True)
    deal = models.ForeignKey(Deal, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantity * self.price_at_purchase



class BankPaymentDetails(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="bank_details")
    phone_used = models.CharField(max_length=20)
    note = models.TextField(blank=True)  # Optional

    def __str__(self):
        return f"Bank Payment for Order #{self.order.id}"


class CashPickupDetails(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="cash_details")
    pickup_name = models.CharField(max_length=100)
    pickup_phone = models.CharField(max_length=20)

    def __str__(self):
        return f"Cash Pickup for Order #{self.order.id}"
