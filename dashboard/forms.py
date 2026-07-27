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