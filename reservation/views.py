from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.models import User
from .models import Reservation

def reservation(request):
    if request.method == "POST":
        user_id = request.session.get('user_id')
        if not user_id:
            messages.error(request, "Please login to make a reservation.")
            return redirect('login')
            
        user = get_object_or_404(User, id=user_id)
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        guests = request.POST.get("guests")
        booking_date = request.POST.get("booking_date")
        booking_time = request.POST.get("booking_time")
        special_request = request.POST.get("special_request")

        Reservation.objects.create(
            user=user,
            name=name,
            phone=phone,
            email=email,
            guests=guests,
            booking_date=booking_date,
            booking_time=booking_time,
            special_request=special_request
        )
        messages.success(request, "Table reserved successfully!")
        return redirect('reservation_list')
        
    return render(request, "reservation/reservation.html")

def reservation_list(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
        
    reservations = Reservation.objects.filter(user_id=user_id).order_by("-id")
    return render(request, "reservation/reservation_list.html", {
        "reservations": reservations
    })

def reservation_detail(request, id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
        
    reservation = get_object_or_404(Reservation, id=id, user_id=user_id)
    return render(request, "reservation/reservation_detail.html", {
        "reservation": reservation
    })