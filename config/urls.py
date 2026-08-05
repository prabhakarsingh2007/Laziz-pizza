from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



from django.views.static import serve

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

# Serve media files in both development and production
urlpatterns += [
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
]
