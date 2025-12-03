from django.contrib import admin
from .models import FavouriteItem

@admin.register(FavouriteItem)
class FavouriteItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_at')
    list_filter = ('added_at', 'user')
    search_fields = ('user__username', 'product__name')



