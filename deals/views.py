from django.shortcuts import render

def deals_page(request):
    return render(request, 'deals/deals.html')
