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

    # Get optional quantity from query parameter, default to 1
    try:
        quantity = int(request.GET.get('quantity', 1))
    except ValueError:
        quantity = 1

    cart_item, created = Cart.objects.get_or_create(
        user=user,
        food=food
    )

    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity
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
    
    from accounts.models import UserAddress
    addresses = UserAddress.objects.filter(user=user).order_by('-id')

    context = {
        "carts": carts,
        "total": total,
        "addresses": addresses,
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
            order = Order.objects.create(
                user=user,
                total_price=total,
                address=address,
                phone=phone
            )
            # Save address to UserAddress if not already saved
            from accounts.models import UserAddress
            if address:
                UserAddress.objects.get_or_create(user=user, address_text=address.strip())
            # Save each cart item as OrderItem
            from orders.models import OrderItem
            for item in carts:
                OrderItem.objects.create(
                    order=order,
                    food=item.food,
                    quantity=item.quantity,
                    price=item.food.price
                )
            # Clear user's cart
            carts.delete()
            return render(request, "cart/order_success.html")
            
    return redirect("cart")