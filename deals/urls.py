from django.urls import path
from . import views

app_name = "deals"

urlpatterns = [
    path('', views.deals, name='deals'),
    path('order-now/<int:deal_id>/', views.order_now_deal, name='order_now_deal'),
]
