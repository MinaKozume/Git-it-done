from django.contrib import admin
<<<<<<< HEAD

# Register your models here.
=======
from .models import Category, MenuItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_editable = ('is_active',)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_active')
    list_filter = ('category', 'is_active')
    list_editable = ('is_active',)
>>>>>>> de4c5ad (Added favourites page)
