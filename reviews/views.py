from django.shortcuts import render
from .models import Review

def reviews_page(request):
    reviews = Review.objects.all().order_by('-date')
    return render(request, 'reviews/reviews.html', {'reviews': reviews})
