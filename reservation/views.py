from django.shortcuts import render, redirect, get_object_or_404
from .models import Reservation


def reservation(request):
    return render(request, "reservation/reservation.html")


def reservation_list(request):
    reservations = Reservation.objects.all()

    return render(request, "reservation/reservation_list.html", {
        "reservations": reservations
    })


def reservation_detail(request, id):
    reservation = get_object_or_404(Reservation, id=id)

    return render(request, "reservation/reservation_detail.html", {
        "reservation": reservation
    })