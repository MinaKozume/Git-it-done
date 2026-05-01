from django.urls import path

from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.reviews_list, name='reviews'),
    path('add/', views.add_review, name='add_review'),
    path('all/', views.reviews_full_list, name='reviews_full_list'),
    path('api/', views.ReviewAPI.as_view(), name='review_api'),
]
