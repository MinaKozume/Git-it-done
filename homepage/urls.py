from django.urls import path

from . import views

app_name = "homepage"

urlpatterns = [
    path('', views.homepage_view, name='homepage'),
    path('api/home/', views.HomeAPI.as_view(), name='home_api'),
]
