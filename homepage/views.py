from django.shortcuts import render 
from menu.models import MenuItem   
from reviews.models import Review 
from deals.models import Deal
from rest_framework.views import APIView
from rest_framework.response import Response

from menu.models import MenuItem
from deals.models import Deal
from reviews.models import Review


def homepage_view(request):
    

    
    try: 
        menu_items = MenuItem.objects.filter(is_active=True)[:3] 
        deals = Deal.objects.filter(is_active=True)[:3]   
        reviews = Review.objects.all().order_by('-date')[:3]  
    except Exception as e:

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
                    "id": d.id,
                    "title": d.title,
                    "price_after": d.price_after,
                    "image": d.image.url if d.image else None
                } for d in deals
            ],

            "latest_reviews": [
                {
                    "id": r.id,
                    "name": r.name,
                    "rating": r.rating,
                    "comment": r.comment
                } for r in latest_reviews
            ]
        })