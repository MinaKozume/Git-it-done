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
    # Allow POST from forms; also accept GET for backward compatibility
    if request.method == 'POST' or request.method == 'GET':
        FavouriteItem.objects.get_or_create(user=request.user, product=product)
        # Redirect back to referring page when possible
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        return redirect("favourites:view_favourites")
    # Fallback
    return redirect("favourites:view_favourites")

@login_required
def remove_from_favourites(request, item_id):
    item = get_object_or_404(FavouriteItem, id=item_id, user=request.user)
    item.delete()
    return redirect("favourites:view_favourites")