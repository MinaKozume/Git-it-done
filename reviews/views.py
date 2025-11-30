from django.shortcuts import render, redirect
from .models import Review
from .forms import ReviewForm  # Assuming you have this form

def reviews_list(request):
    # Use 'date' instead of 'created_at'
    latest_three = Review.objects.order_by('-date')[:3]
    all_reviews = Review.objects.order_by('-date')
    
    return render(request, 'reviews/reviews.html', {
        "latest_three": latest_three,
        "all_reviews": all_reviews
    })

def add_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("reviews:reviews")  # Redirect to the reviews list after adding
    else:
        form = ReviewForm()

    return render(request, "reviews/add_review.html", {"form": form})

def reviews_full_list(request):
    # Use 'date' instead of 'created_at'
    all_reviews = Review.objects.order_by('-date')
    
    return render(request, 'reviews/reviews_full_list.html', {
        "all_reviews": all_reviews
    })
