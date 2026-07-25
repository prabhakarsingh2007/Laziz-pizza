from django.urls import path
from . import views

urlpatterns = [
    path("", views.cart, name="cart"),
    path("add/<int:id>/", views.add_to_cart, name="add_to_cart"),
    path("remove/<int:id>/", views.remove_from_cart, name="remove_from_cart"),
    path("update/<int:id>/", views.update_quantity, name="update_quantity"),
    path("checkout/", views.checkout, name="checkout"),
    path("success/", views.order_success, name="order_success"),
]