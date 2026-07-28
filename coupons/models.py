from django.db import models
from accounts.models import User
from menu.models import Category, FoodItem
from orders.models import Order


class Coupon(models.Model):
    DISCOUNT_CHOICES = [
        ('Percentage', 'Percentage'),
        ('Fixed Amount', 'Fixed Amount'),
    ]

    code = models.CharField(max_length=50, unique=True, db_index=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    maximum_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    start_date = models.DateTimeField()
    expiry_date = models.DateTimeField()
    active = models.BooleanField(default=True)
    
    usage_limit = models.PositiveIntegerField(null=True, blank=True, help_text="Maximum total times this coupon can be used")
    used_count = models.PositiveIntegerField(default=0)
    one_time_per_user = models.BooleanField(default=True)
    
    applicable_categories = models.ManyToManyField(Category, blank=True, related_name='applicable_coupons')
    applicable_products = models.ManyToManyField(FoodItem, blank=True, related_name='applicable_coupons')
    excluded_products = models.ManyToManyField(FoodItem, blank=True, related_name='excluded_coupons')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.code:
            self.code = self.code.upper().strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} ({self.discount_type}: {self.discount_value})"


class CouponUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coupon_usages')
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='usages')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='coupon_usages')
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    used_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} used {self.coupon.code} for Order #{self.order.id}"
