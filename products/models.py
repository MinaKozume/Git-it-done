from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.CharField(max_length=100, blank=True)  # e.g. coffee, pastry
    is_popular = models.BooleanField(default=False)

    def __str__(self):
        return self.name
