from django.shortcuts import render, redirect  
from .models import FAQ
from .forms import ContactUsForm

def about(request):

    faqs = FAQ.objects.all()


    coffee_shop_name = 'KAFEI'  
    form = ContactUsForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('about:about') 

    return render(request, 'about/about.html', {
        'faqs': faqs,
        'form': form,
        'coffee_shop_name': coffee_shop_name,
        'user': request.user
    })
