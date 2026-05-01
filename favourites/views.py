from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from menu.models import MenuItem
from .models import FavouriteItem
from .serializers import FavouriteSerializer


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


class FavouriteListCreateAPI(ListCreateAPIView):
    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FavouriteItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavouriteDeleteAPI(DestroyAPIView):
    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FavouriteItem.objects.filter(user=self.request.user)
