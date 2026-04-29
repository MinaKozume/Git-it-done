from django.urls import path
from . import views
from .views import menu_page, menu_item_detail, MenuListAPI

app_name = "menu"

urlpatterns = [
    path('', views.menu_page, name="menu_home"),
    path('item/<int:item_id>/', views.menu_item_detail, name='menu_item_detail'),

   
    path('api/', MenuListAPI.as_view(), name='menu_api'),
]