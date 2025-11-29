from django.urls import path
from . import views

app_name = "menu"

urlpatterns = [
<<<<<<< HEAD
    path('', views.menu_view, name='menu_home'),
=======
    path('', views.menu_page, name="menu_home"),
    path('item/<int:item_id>/', views.menu_item_detail, name='menu_item_detail'),
>>>>>>> de4c5ad (Added favourites page)
]
