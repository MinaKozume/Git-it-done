from django.urls import path
from . import views
from django.urls import path
from . import views
from .views import AboutAPI

app_name = "about"

urlpatterns = [
    path('', views.about, name='about'),
    path('api/', AboutAPI.as_view(), name='about_api'),
]


