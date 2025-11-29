from django.db import models
from django.contrib.auth.models import User
from menu.models import MenuItem

class FavouriteItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favourites")
    product = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # Prevent duplicates

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
