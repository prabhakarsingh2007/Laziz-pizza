from django import forms
from menu.models import FoodItem
from home.models import PopularItem

class FoodForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-red-500 outline-none'}),
            'category': forms.Select(attrs={'class': 'w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-red-500 outline-none'}),
            'food_type': forms.Select(attrs={'class': 'w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-red-500 outline-none'}),
            'price': forms.NumberInput(attrs={'class': 'w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-red-500 outline-none'}),
            'image': forms.ClearableFileInput(attrs={'class': 'w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-red-500 outline-none'}),
            'description': forms.Textarea(attrs={'class': 'w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-red-500 outline-none', 'rows': 4}),
            'available': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-red-600 border-gray-300 rounded focus:ring-red-500'}),
        }


class PopularItemForm(forms.ModelForm):
    class Meta:
        model = PopularItem
        fields = ['name', 'subtitle', 'price', 'category', 'image', 'order', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-red-500 outline-none', 'placeholder': 'e.g. Margherita Pizza'}),
            'subtitle': forms.TextInput(attrs={'class': 'w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-red-500 outline-none', 'placeholder': 'e.g. Cheese Loaded Pizza'}),
            'price': forms.NumberInput(attrs={'class': 'w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-red-500 outline-none', 'placeholder': 'e.g. 299'}),
            'category': forms.Select(attrs={'class': 'w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-red-500 outline-none'}),
            'image': forms.ClearableFileInput(attrs={'class': 'w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-red-500 outline-none'}),
            'order': forms.NumberInput(attrs={'class': 'w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-red-500 outline-none', 'placeholder': 'e.g. 1'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-red-600 border-gray-300 rounded focus:ring-red-500'}),
        }


from coupons.models import Coupon

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = [
            'code', 'name', 'description', 'discount_type', 'discount_value',
            'minimum_order_amount', 'maximum_discount_amount', 'start_date',
            'expiry_date', 'active', 'usage_limit', 'one_time_per_user',
            'applicable_categories', 'applicable_products', 'excluded_products'
        ]
        widgets = {
            'code': forms.TextInput(attrs={'class': 'w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-red-500 outline-none', 'placeholder': 'e.g. SAVE20'}),
            'name': forms.TextInput(attrs={'class': 'w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-red-500 outline-none', 'placeholder': 'e.g. 20% Discount'}),
            'description': forms.Textarea(attrs={'class': 'w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-red-500 outline-none', 'rows': 2, 'placeholder': 'Optional description'}),
            'discount_type': forms.Select(attrs={'class': 'w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-red-500 outline-none'}),
            'discount_value': forms.NumberInput(attrs={'class': 'w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-red-500 outline-none', 'placeholder': 'e.g. 20 or 100'}),
            'minimum_order_amount': forms.NumberInput(attrs={'class': 'w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-red-500 outline-none', 'placeholder': 'e.g. 200'}),
            'maximum_discount_amount': forms.NumberInput(attrs={'class': 'w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-red-500 outline-none', 'placeholder': 'e.g. 500 (Optional)'}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-red-500 outline-none'}),
            'expiry_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-red-500 outline-none'}),
            'active': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-red-600 border-gray-300 rounded focus:ring-red-500'}),
            'usage_limit': forms.NumberInput(attrs={'class': 'w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-red-500 outline-none', 'placeholder': 'e.g. 100 (Optional)'}),
            'one_time_per_user': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-red-600 border-gray-300 rounded focus:ring-red-500'}),
            'applicable_categories': forms.SelectMultiple(attrs={'class': 'w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-red-500 outline-none', 'style': 'height: 120px;'}),
            'applicable_products': forms.SelectMultiple(attrs={'class': 'w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-red-500 outline-none', 'style': 'height: 120px;'}),
            'excluded_products': forms.SelectMultiple(attrs={'class': 'w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-red-500 outline-none', 'style': 'height: 120px;'}),
        }