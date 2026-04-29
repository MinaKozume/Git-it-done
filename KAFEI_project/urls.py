from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('menu/', include('menu.urls')),
    path('reviews/', include('reviews.urls')),
    path('deals/', include('deals.urls')),
    path('about/', include('about.urls')),
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("cart/", include("cart.urls")),
    path("order/", include("orders.urls")),
    path('favourites/', include('favourites.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
