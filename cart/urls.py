from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("", views.view_cart, name="view_cart"),
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("add-deal/<int:deal_id>/", views.add_deal_to_cart, name="add_deal_to_cart"),
    path("update/<int:item_id>/", views.update_quantity, name="update_quantity"),
    path("remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path('api/', views.cart_list_api, name='cart_api'),
    path('api/add/', views.add_to_cart_api, name='cart_add_api'),
    path('api/remove/<int:item_id>/', views.remove_from_cart_api, name='cart_remove_api'),
]
