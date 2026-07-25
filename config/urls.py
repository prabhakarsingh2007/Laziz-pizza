
from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("menu/", include("menu.urls")),
    path("", include("home.urls")),
    path("cart/", include("cart.urls")),
    path("orders/", include("orders.urls")),
    path("reservation/", include("reservation.urls")),
    path("dashboard/", include("dashboard.urls")),
]
