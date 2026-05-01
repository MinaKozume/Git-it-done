from django.urls import path

from . import views

app_name = "about"

urlpatterns = [
    path('', views.about, name='about'),
    path('api/', views.AboutAPI.as_view(), name='about_api'),
]
