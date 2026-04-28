from django.db import models
from django.contrib.auth.models import User
from menu.models import MenuItem
from deals.models import Deal

class CartItem(models.Model):
    ITEM_CHOICES = (
        ('MENU', 'Menu Item'),
        ('DEAL', 'Deal'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(MenuItem, null=True, blank=True, on_delete=models.CASCADE)
    deal = models.ForeignKey(Deal, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_type = models.CharField(max_length=10, choices=ITEM_CHOICES)

    def subtotal(self):
        if self.item_type == 'MENU' and self.product:
            return self.product.price * self.quantity
        elif self.item_type == 'DEAL' and self.deal:
            return self.deal.price_after * self.quantity
        return 0
