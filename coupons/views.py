import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from accounts.models import User
from cart.models import Cart
from .services import validate_and_calculate_discount
from .models import Coupon

@csrf_exempt
def apply_coupon(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)

    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"success": False, "message": "Please login to apply coupons."}, status=401)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"success": False, "message": "User session invalid."}, status=401)

    try:
        data = json.loads(request.body)
        coupon_code = data.get("coupon_code", "").upper().strip()
    except (ValueError, TypeError):
        return JsonResponse({"success": False, "message": "Invalid post data."}, status=400)

    if not coupon_code:
        return JsonResponse({"success": False, "message": "Coupon code cannot be empty."}, status=400)

    # Get cart items and subtotal
    cart_items = Cart.objects.filter(user=user)
    cart_total = sum(item.total_price() for item in cart_items)

    if not cart_items.exists():
        return JsonResponse({"success": False, "message": "Your cart is empty."}, status=400)

    is_valid, discount_amount, message = validate_and_calculate_discount(
        coupon_code=coupon_code,
        user=user,
        cart_items=cart_items,
        cart_total=cart_total
    )

    if not is_valid:
        return JsonResponse({"success": False, "message": message})

    # Save to session
    request.session["coupon_code"] = coupon_code
    final_total = max(float(cart_total) - float(discount_amount), 0.0)

    return JsonResponse({
        "success": True,
        "message": "Coupon applied successfully!",
        "discount": float(discount_amount),
        "final_total": final_total
    })


@csrf_exempt
def remove_coupon(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)

    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"success": False, "message": "Please login."}, status=401)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"success": False, "message": "User session invalid."}, status=401)

    # Remove from session
    if "coupon_code" in request.session:
        del request.session["coupon_code"]

    cart_items = Cart.objects.filter(user=user)
    cart_total = sum(item.total_price() for item in cart_items)

    return JsonResponse({
        "success": True,
        "message": "Coupon removed successfully.",
        "discount": 0.0,
        "final_total": float(cart_total)
    })
