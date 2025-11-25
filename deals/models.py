from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Deal(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price_before = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    price_after = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='deals/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

