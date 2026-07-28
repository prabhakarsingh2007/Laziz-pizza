from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("cart/", include("cart.urls")),
    path("coupon/", include("coupons.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("orders/", include("orders.urls")),
    path("reservation/", include("reservation.urls")),
    path("menu/", include("menu.urls")),
    path("", include("home.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
