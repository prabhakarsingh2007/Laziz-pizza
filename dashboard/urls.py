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
    path("reservations/update/<int:id>/", views.update_reservation_status, name="update_reservation_status"),

    # Category Management
    path("categories/", views.category_list, name="category_list"),
    path("categories/delete/<int:id>/", views.delete_category, name="delete_category"),

    # Popular Cards Management
    path("popular/", views.popular_list, name="popular_list"),
    path("popular/edit/<int:id>/", views.edit_popular, name="edit_popular"),
    path("popular/delete/<int:id>/", views.delete_popular, name="delete_popular"),

    # Order Count API (AJAX Polling)
    path("order-count/", views.order_count, name="order_count"),

    # Coupon & Offer Management
    path("coupons/", views.coupon_list, name="coupon_list"),
    path("coupons/edit/<int:id>/", views.edit_coupon, name="edit_coupon"),
    path("coupons/delete/<int:id>/", views.delete_coupon, name="delete_coupon"),

    # User Management
    path("users/", views.admin_users, name="admin_users"),
]