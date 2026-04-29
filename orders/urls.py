from django.urls import path
from . import views
from .views import OrderListAPI


app_name = "orders"

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("place-order/", views.place_order, name="place_order"),
    path("success/", views.success, name="success"),
    path("history/", views.order_history, name="order_history"),  
    path('api/history/', OrderListAPI.as_view(), name='order_api_history'),
]
