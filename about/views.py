from django.shortcuts import render, redirect  # Added redirect
from .models import FAQ
from .forms import ContactUsForm

def about(request):
    # Get the FAQs from the database
    faqs = FAQ.objects.all()

    # Pass the logged-in user's username and coffee shop name to the template
    coffee_shop_name = 'KAFEI'  # You can modify this to be dynamic if needed

    form = ContactUsForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('about:about')  # Redirect to avoid re-submitting the form

    return render(request, 'about/about.html', {
        'faqs': faqs,
        'form': form,
        'coffee_shop_name': coffee_shop_name,
        'user': request.user
    })
