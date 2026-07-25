from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart
from menu.models import FoodItem
from accounts.models import User


# Cart Page
def cart(request):
    carts = Cart.objects.all()
    total = sum(item.total_price() for item in carts)

    context = {
        "carts": carts,
        "total": total,
    }

    return render(request, "cart/cart.html", context)


# Add To Cart
def add_to_cart(request, id):
    food = get_object_or_404(FoodItem, id=id)

    user = User.objects.first()   # Temporary (Login System complete hone ke baad request.user use karenge)

    cart_item, created = Cart.objects.get_or_create(
        user=user,
        food=food
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart")


# Remove From Cart
def remove_from_cart(request, id):
    cart_item = get_object_or_404(Cart, id=id)
    cart_item.delete()

    return redirect("cart")


# Update Quantity
def update_quantity(request, id):
    cart_item = get_object_or_404(Cart, id=id)

    if request.method == "POST":
        quantity = request.POST.get("quantity")

        if quantity:
            cart_item.quantity = int(quantity)
            cart_item.save()

    return redirect("cart")


# Checkout Page
def checkout(request):
    carts = Cart.objects.all()
    total = sum(item.total_price() for item in carts)

    context = {
        "carts": carts,
        "total": total,
    }

    return render(request, "cart/checkout.html", context)


# Order Success
def order_success(request):
    return render(request, "cart/order_success.html")