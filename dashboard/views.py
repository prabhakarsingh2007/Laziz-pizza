from django.shortcuts import render
from accounts.models import User
from menu.models import FoodItem
from orders.models import Order
from reservation.models import Reservation


def dashboard(request):

    context = {
        "total_users": User.objects.count(),
        "total_foods": FoodItem.objects.count(),
        "total_orders": Order.objects.count(),
        "total_reservations": Reservation.objects.count(),
        "recent_orders": Order.objects.all().order_by("-id")[:5],
        "recent_reservations": Reservation.objects.all().order_by("-id")[:5],
    }

    return render(request, "dashboard/dashboard.html", context)