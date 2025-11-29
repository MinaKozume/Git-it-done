from django.db import models

<<<<<<< HEAD
# Create your models here.
=======
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name




>>>>>>> de4c5ad (Added favourites page)
