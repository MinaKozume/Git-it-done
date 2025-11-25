from django.shortcuts import render
from .models import Deal, Category
from datetime import date

def deals(request):
    today = date.today()
    categories = Category.objects.all()

    # Get deals per category
    category_deals = {}
    for cat in categories:
        deals_in_cat = Deal.objects.filter(is_active=True, category=cat).order_by('-start_date')
        category_deals[cat.name] = deals_in_cat

    context = {
        'category_deals': category_deals,
        'today': today
    }

    return render(request, 'deals/deals.html', context)
