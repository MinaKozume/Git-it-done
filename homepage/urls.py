from django.urls import path
from . import views
from django.urls import path
from .views import HomeAPI

app_name = "homepage"

urlpatterns = [
    path('', views.homepage_view, name='homepage'),
    path('api/home/', HomeAPI.as_view(), name='home_api'),
]



