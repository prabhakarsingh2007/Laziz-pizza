from django.shortcuts import render, redirect
from accounts.models import User
from .models import Order

def my_orders(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
        
    orders = Order.objects.filter(user_id=user_id).order_by("-id")
    return render(request, "orders/order_list.html", {
        "orders": orders
    })

def order_detail(request, id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
        
    order = Order.objects.get(id=id, user_id=user_id)
    return render(request, "orders/order_detail.html", {
        "order": order
    })