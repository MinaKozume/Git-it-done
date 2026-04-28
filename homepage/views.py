from django.shortcuts import render 
from menu.models import MenuItem   
from reviews.models import Review 
from deals.models import Deal

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