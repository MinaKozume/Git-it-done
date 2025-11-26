from django.shortcuts import render, get_object_or_404
from .models import Category, MenuItem

def menu_page(request):
    categories = Category.objects.filter(is_active=True)
    items_by_category = {}

    # Get filter/search/sort values
    selected_category = request.GET.get('category')
    price_filter = request.GET.get('price')
    sort_option = request.GET.get('sort')
    search_query = request.GET.get('search')

    for cat in categories:
        items = MenuItem.objects.filter(category=cat, is_active=True)

        # Filter by category if selected
        if selected_category and selected_category != 'all':
            if str(cat.id) != selected_category:
                items = MenuItem.objects.none()

        # Filter by price
        if price_filter:
            if price_filter == 'lt100':
                items = items.filter(price__lt=100)
            elif price_filter == '100to200':
                items = items.filter(price__gte=100, price__lte=200)
            elif price_filter == 'gt200':
                items = items.filter(price__gt=200)

        # Search by name or description
        if search_query:
            items = items.filter(name__icontains=search_query) | items.filter(description__icontains=search_query)

        # Sorting
        if sort_option == 'price_asc':
            items = items.order_by('price')
        elif sort_option == 'price_desc':
            items = items.order_by('-price')

        items_by_category[cat] = items

    return render(request, "menu/menu.html", {
        "categories": categories,
        "items_by_category": items_by_category,
        "selected_category": selected_category,
        "price_filter": price_filter,
        "sort_option": sort_option,
        "search_query": search_query,
    })


def menu_item_detail(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    return render(request, 'menu/menu_item_detail.html', {'item': item})


