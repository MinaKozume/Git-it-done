from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("place-order/", views.place_order, name="place_order"),
    path("success/", views.success, name="success"),
]
