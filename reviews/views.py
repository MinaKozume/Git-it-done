from django.shortcuts import render, redirect
from django.db.models import Avg
from .models import Review
from .forms import ReviewForm  

def reviews_list(request):
    
    latest_three = Review.objects.order_by('-date')[:3]
    all_reviews = Review.objects.order_by('-date')

    
    total_reviews = all_reviews.count()
    average_rating = all_reviews.aggregate(Avg('rating'))['rating__avg'] or 0 

    context = {
        "latest_three": latest_three,
        "all_reviews": all_reviews,
        "total_reviews": total_reviews,
        "average_rating": round(average_rating, 1),  
    }
    return render(request, 'reviews/reviews.html', context)


def add_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("reviews:reviews") 
    else:
        form = ReviewForm()

    return render(request, "reviews/add_review.html", {"form": form})


def reviews_full_list(request):
   
    all_reviews = Review.objects.order_by('-date')


    total_reviews = all_reviews.count()
    average_rating = all_reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    context = {
        "all_reviews": all_reviews,
        "total_reviews": total_reviews,
        "average_rating": round(average_rating, 1),
    }
    return render(request, 'reviews/reviews_full_list.html', context)
