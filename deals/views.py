from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.generics import ListAPIView

from .models import Deal, Category
from .serializers import DealSerializer
from cart.views import add_deal_to_cart


def deals(request):
    today = date.today()
    categories = Category.objects.all()

    category_deals = {}
    for cat in categories:
        deals_in_cat = Deal.objects.filter(is_active=True, category=cat).order_by('-start_date')
        category_deals[cat.name] = deals_in_cat

    context = {
        'category_deals': category_deals,
        'today': today
    }

    return render(request, 'deals/deals.html', context)


def order_now_deal(request, deal_id):
    deal = get_object_or_404(Deal, id=deal_id, is_active=True)
    add_deal_to_cart(request, deal.id)
    return redirect('orders:checkout')


class DealAPI(ListAPIView):
    queryset = Deal.objects.filter(is_active=True)
    serializer_class = DealSerializer
