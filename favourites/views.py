from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from menu.models import MenuItem
from .models import FavouriteItem

@login_required
def view_favourites(request):
    items = FavouriteItem.objects.filter(user=request.user)
    return render(request, "favourites/favourites.html", {"items": items})

@login_required
def add_to_favourites(request, product_id):
    product = get_object_or_404(MenuItem, id=product_id)
    FavouriteItem.objects.get_or_create(user=request.user, product=product)
    return redirect("favourites:view_favourites")

@login_required
def remove_from_favourites(request, item_id):
    item = get_object_or_404(FavouriteItem, id=item_id, user=request.user)
    item.delete()
    return redirect("favourites:view_favourites")