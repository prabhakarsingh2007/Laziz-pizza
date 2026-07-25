from django.urls import path
from . import views

urlpatterns = [
    path("", views.reservation, name="reservation"),
    path("list/", views.reservation_list, name="reservation_list"),
    path("<int:id>/", views.reservation_detail, name="reservation_detail"),
]