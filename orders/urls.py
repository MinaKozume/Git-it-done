from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("place-order/", views.place_order, name="place_order"),
    path("success/", views.success, name="success"),
    path("history/", views.order_history, name="order_history"),
    path("api/history/", views.OrderListAPI.as_view(), name="order_api_history"),
    path("api/place/", views.place_order_api, name="order_api_place"),
    path("api/latest/", views.latest_order_api, name="order_api_latest"),
]
