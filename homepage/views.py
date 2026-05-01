from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from menu.models import MenuItem
from reviews.models import Review
from deals.models import Deal


def homepage_view(request):
    try:
        menu_items = MenuItem.objects.filter(is_active=True)[:3]
        deals = Deal.objects.filter(is_active=True)[:3]
        reviews = Review.objects.all().order_by('-date')[:3]
    except Exception:
        menu_items = []
        deals = []
        reviews = []

    context = {
        'menu_items': menu_items,
        'deals': deals,
        'reviews': reviews,
    }
    return render(request, 'homepage/home.html', context)


class HomeAPI(APIView):
    def get(self, request):
        featured_menu = MenuItem.objects.filter(is_active=True)[:6]
        deals = Deal.objects.filter(is_active=True)[:5]
        latest_reviews = Review.objects.order_by('-date')[:5]

        return Response({
            "featured_menu": [
                {
                    "id": item.id,
                    "name": item.name,
                    "price": item.price,
                    "image": item.image.url if item.image else None
                } for item in featured_menu
            ],
            "active_deals": [
                {
                    "id": deal.id,
                    "title": deal.title,
                    "price_after": deal.price_after,
                    "image": deal.image.url if deal.image else None
                } for deal in deals
            ],
            "latest_reviews": [
                {
                    "id": review.id,
                    "name": review.name,
                    "rating": review.rating,
                    "comment": review.comment
                } for review in latest_reviews
            ]
        })
