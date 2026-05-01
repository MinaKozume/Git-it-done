from django.contrib import admin
from .models import Deal, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price_after', 'is_active', 'start_date', 'end_date')
    list_filter = ('category', 'is_active')

