from django.urls import path
from . import views
from .views import DealAPI

app_name = "deals"

urlpatterns = [
    path('', views.deals, name='deals'),
    path('order-now/<int:deal_id>/', views.order_now_deal, name='order_now_deal'),


    path('api/', DealAPI.as_view(), name='deal_api'),
]