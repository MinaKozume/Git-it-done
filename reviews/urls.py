from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.reviews_list, name='reviews'),  # Main reviews page (carousel of recent reviews)
    path('add/', views.add_review, name='add_review'),  # Add a new review
    path('all/', views.reviews_full_list, name='reviews_full_list'),  # Full list of reviews
]
