import datetime
from django.utils import timezone
from django.db.models import Q
from .models import Coupon, CouponUsage

def validate_and_calculate_discount(coupon_code, user, cart_items, cart_total):
    """
    Validates the coupon against user, cart items, and total price.
    Returns: (is_valid, discount_amount, message)
    """
    coupon_code = coupon_code.upper().strip()
    try:
        coupon = Coupon.objects.get(code=coupon_code)
    except Coupon.DoesNotExist:
        return False, 0, "Invalid coupon code."

    # 1. Active Check
    if not coupon.active:
        return False, 0, "This coupon is inactive."

    # 2. Date/Expiry Check
    now = timezone.now()
    if now < coupon.start_date:
        return False, 0, "Coupon has not started yet."
    if now > coupon.expiry_date:
        return False, 0, "Coupon has expired."

    # 3. Minimum Order Amount Check
    if cart_total < coupon.minimum_order_amount:
        return False, 0, f"Minimum order of ₹{coupon.minimum_order_amount:.0f} required."

    # 4. Global Usage Limit Check
    if coupon.usage_limit is not None and coupon.used_count >= coupon.usage_limit:
        return False, 0, "Usage limit exceeded for this coupon."

    # 5. One Time Per User Check
    if coupon.one_time_per_user and user:
        if CouponUsage.objects.filter(user=user, coupon=coupon).exists():
            return False, 0, "You have already used this coupon."

    # 6. Item-level Applicability Checks
    # We calculate the subtotal of eligible items
    has_applicability_restrictions = (
        coupon.applicable_categories.exists() or 
        coupon.applicable_products.exists() or 
        coupon.excluded_products.exists()
    )

    eligible_subtotal = 0
    any_item_eligible = False

    for item in cart_items:
        product = item.food
        # Check exclusion first
        if coupon.excluded_products.filter(id=product.id).exists():
            continue

        # Check product level inclusion
        product_eligible = True
        if coupon.applicable_products.exists():
            if not coupon.applicable_products.filter(id=product.id).exists():
                product_eligible = False

        # Check category level inclusion
        category_eligible = True
        if coupon.applicable_categories.exists():
            if not coupon.applicable_categories.filter(id=product.category.id).exists():
                category_eligible = False

        if product_eligible and category_eligible:
            eligible_subtotal += item.total_price()
            any_item_eligible = True

    if has_applicability_restrictions and not any_item_eligible:
        return False, 0, "This coupon is not applicable to the items in your cart."

    # If no restrictions, the entire cart_total is the eligible subtotal
    subtotal_for_discount = eligible_subtotal if has_applicability_restrictions else cart_total

    # Calculate discount amount
    discount_amount = 0
    if coupon.discount_type == 'Percentage':
        discount_amount = (coupon.discount_value / 100) * subtotal_for_discount
    elif coupon.discount_type == 'Fixed Amount':
        discount_amount = coupon.discount_value

    # Apply maximum discount cap
    if coupon.maximum_discount_amount is not None:
        discount_amount = min(discount_amount, coupon.maximum_discount_amount)

    # Discount can never exceed the total price
    discount_amount = min(discount_amount, cart_total)

    # Return success
    return True, round(discount_amount, 2), "Coupon applied successfully"
