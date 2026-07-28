from django.contrib import admin
from .models import Coupon, CouponUsage

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = [
        'code', 'name', 'discount_type', 'discount_value', 
        'minimum_order_amount', 'start_date', 'expiry_date', 
        'active', 'usage_limit', 'used_count'
    ]
    list_filter = ['active', 'discount_type', 'start_date', 'expiry_date']
    search_fields = ['code', 'name', 'description']
    ordering = ['-created_at']
    actions = ['activate_coupons', 'deactivate_coupons']

    filter_horizontal = ['applicable_categories', 'applicable_products', 'excluded_products']

    def activate_coupons(self, request, queryset):
        queryset.update(active=True)
        self.message_user(request, "Selected coupons have been activated.")
    activate_coupons.short_description = "Activate selected coupons"

    def deactivate_coupons(self, request, queryset):
        queryset.update(active=False)
        self.message_user(request, "Selected coupons have been deactivated.")
    deactivate_coupons.short_description = "Deactivate selected coupons"


@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):
    list_display = ['user', 'coupon', 'order', 'discount_amount', 'used_at']
    list_filter = ['used_at', 'coupon__discount_type']
    search_fields = ['user__username', 'coupon__code', 'order__id']
    ordering = ['-used_at']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
