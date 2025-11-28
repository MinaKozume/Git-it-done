from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('menu/', include('menu.urls')),
    path('reviews/', include('reviews.urls')),
    path('deals/', include('deals.urls')),
    path('about/', include('about.urls')),
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("cart/", include("cart.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
