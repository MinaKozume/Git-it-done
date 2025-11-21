from django.shortcuts import render

def menu_view(request):
    # example data you might pass to template
    coffee_items = [
        {'name': 'Espresso', 'price': 2.50},
        {'name': 'Cappuccino', 'price': 3.50},
        {'name': 'Latte', 'price': 3.75},
    ]
    return render(request, 'menu/menu_home.html', {'coffee_items': coffee_items})
