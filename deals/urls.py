from django.urls import path
from . import views

app_name = 'deals'

urlpatterns = [
    path('', views.deals_page, name='deals'),
]