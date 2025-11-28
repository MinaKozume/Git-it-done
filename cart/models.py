from django.db import models
from django.contrib.auth.models import User
from menu.models import MenuItem

# A cart item represents ONE product in a user's cart
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity} ({self.user.username})"

    class Meta:
        unique_together = ('user', 'product')  # prevents duplicate cart entries
