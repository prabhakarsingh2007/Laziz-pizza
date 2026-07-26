from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("foods/", views.food_list, name="food_list"),
    path("foods/add/", views.add_food, name="add_food"),
    path("foods/edit/<int:id>/", views.edit_food, name="edit_food"),
    path("foods/delete/<int:id>/", views.delete_food, name="delete_food"),
    path("orders/", views.admin_orders, name="admin_orders"),
    path("reservations/", views.admin_reservations, name="admin_reservations"),
    path("users/", views.admin_users, name="admin_users"),
]