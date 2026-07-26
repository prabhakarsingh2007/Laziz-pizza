from cart.models import Cart

def laziz_context(request):
    cart_count = 0
    user_id = request.session.get('user_id')
    if user_id:
        cart_count = Cart.objects.filter(user_id=user_id).count()
    return {
        'restaurant_name': 'Laziz Pizza',
        'cart_count': cart_count,
    }
