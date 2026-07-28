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

    revalidate_session_coupon(request)
    return redirect("cart")


# Remove From Cart
def remove_from_cart(request, id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
        
    cart_item = get_object_or_404(Cart, id=id, user_id=user_id)
    cart_item.delete()

    revalidate_session_coupon(request)
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

    revalidate_session_coupon(request)
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
            coupon_code = request.session.get("coupon_code")
            discount_amount = 0
            applied_coupon = None

            if coupon_code:
                from coupons.services import validate_and_calculate_discount
                from coupons.models import Coupon, CouponUsage
                is_valid, calc_discount, message = validate_and_calculate_discount(
                    coupon_code=coupon_code,
                    user=user,
                    cart_items=carts,
                    cart_total=total
                )
                if is_valid:
                    discount_amount = calc_discount
                    applied_coupon = Coupon.objects.get(code=coupon_code.upper().strip())
                    
                    from django.db import transaction
                    with transaction.atomic():
                        db_coupon = Coupon.objects.select_for_update().get(id=applied_coupon.id)
                        db_coupon.used_count += 1
                        db_coupon.save()

            final_price = max(total - discount_amount, 0)

            # Save the Order
            order = Order.objects.create(
                user=user,
                total_price=final_price,
                original_total=total,
                discount=discount_amount,
                coupon=applied_coupon,
                coupon_code=coupon_code.upper().strip() if coupon_code else None,
                address=address,
                phone=phone
            )
            # Save address to UserAddress if not already saved
            from accounts.models import UserAddress
            if address:
                UserAddress.objects.get_or_create(user=user, address_text=address.strip())

            # Record CouponUsage
            if applied_coupon:
                CouponUsage.objects.create(
                    user=user,
                    coupon=applied_coupon,
                    order=order,
                    discount_amount=discount_amount
                )
                request.session.pop("coupon_code", None)
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


def revalidate_session_coupon(request):
    coupon_code = request.session.get("coupon_code")
    if not coupon_code:
        return

    user_id = request.session.get("user_id")
    if not user_id:
        request.session.pop("coupon_code", None)
        return

    from accounts.models import User
    from cart.models import Cart
    from coupons.services import validate_and_calculate_discount
    from django.contrib import messages

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        request.session.pop("coupon_code", None)
        return

    cart_items = Cart.objects.filter(user=user)
    cart_total = sum(item.total_price() for item in cart_items)

    is_valid, _, message = validate_and_calculate_discount(
        coupon_code=coupon_code,
        user=user,
        cart_items=cart_items,
        cart_total=cart_total
    )

    if not is_valid:
        request.session.pop("coupon_code", None)
        messages.warning(request, f"Coupon '{coupon_code}' was removed: {message}")