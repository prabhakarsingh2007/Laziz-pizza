from django.urls import path
from . import views

urlpatterns = [
    path("", views.my_orders, name="my_orders"),
    path("<int:id>/", views.order_detail, name="order_detail"),
]