from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path("", views.dashboard, name="dashboard"),

    # Food Management
    path("foods/", views.food_list, name="food_list"),
    path("foods/add/", views.add_food, name="add_food"),
    path("foods/edit/<int:id>/", views.edit_food, name="edit_food"),
    path("foods/delete/<int:id>/", views.delete_food, name="delete_food"),

    # Order Management
    path("orders/", views.admin_orders, name="admin_orders"),
    path("orders/<int:id>/", views.order_detail, name="order_detail"),
    path("orders/update/<int:id>/", views.update_order_status, name="update_order_status"),
    path("sales/", views.sales, name="sales"),

    # Reservation Management
    path("reservations/", views.admin_reservations, name="admin_reservations"),

    # User Management
    path("users/", views.admin_users, name="admin_users"),
]