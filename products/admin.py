from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_popular')
    list_filter = ('category', 'is_popular')
    search_fields = ('name',)
