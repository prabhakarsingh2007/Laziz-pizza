from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart
from menu.models import FoodItem
from accounts.models import User
from orders.models import Order

# Cart Page
def cart(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
        
    user = get_object_or_404(User, id=user_id)
    carts = Cart.objects.filter(user=user)
    total = sum(item.total_price() for item in carts)

    context = {
        "carts": carts,
        "total": total,
    }

    return render(request, "cart/cart.html", context)


# Add To Cart
def add_to_cart(request, id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
        
    user = get_object_or_404(User, id=user_id)
    food = get_object_or_404(FoodItem, id=id)

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
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
        
    cart_item = get_object_or_404(Cart, id=id, user_id=user_id)
    cart_item.delete()

    return redirect("cart")


# Update Quantity
def update_quantity(request, id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
        
    cart_item = get_object_or_404(Cart, id=id, user_id=user_id)

    if request.method == "POST":
        quantity = request.POST.get("quantity")
        if quantity:
            cart_item.quantity = int(quantity)
            cart_item.save()

    return redirect("cart")


# Checkout Page
def checkout(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
        
    user = get_object_or_404(User, id=user_id)
    carts = Cart.objects.filter(user=user)
    total = sum(item.total_price() for item in carts)

    context = {
        "carts": carts,
        "total": total,
    }

    return render(request, "cart/checkout.html", context)


# Order Success / Order Placement
def order_success(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
        
    user = get_object_or_404(User, id=user_id)
    carts = Cart.objects.filter(user=user)
    
    if request.method == "POST":
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        total = sum(item.total_price() for item in carts)
        
        if total > 0:
            # Save the Order
            Order.objects.create(
                user=user,
                total_price=total,
                address=address,
                phone=phone
            )
            # Clear user's cart
            carts.delete()
            return render(request, "cart/order_success.html")
            
    return redirect("cart")