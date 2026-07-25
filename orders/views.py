from django.shortcuts import render
from .models import Order


def my_orders(request):
    orders = Order.objects.all()

    return render(request, "orders/my_orders.html", {
        "orders": orders
    })


def order_detail(request, id):
    order = Order.objects.get(id=id)

    return render(request, "orders/order_detail.html", {
        "order": order
    })