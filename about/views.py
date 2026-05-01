from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import FAQ
from .forms import ContactUsForm
from .serializers import FAQSerializer


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


class AboutAPI(APIView):
    def get(self, request):
        faqs = FAQ.objects.all()
        serializer = FAQSerializer(faqs, many=True)

        return Response({
            "app_name": "KAFEI",
            "description": "Coffee ordering app with menu, cart, deals, reviews, orders and location features.",
            "faqs": serializer.data
        })
