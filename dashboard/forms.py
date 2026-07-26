from django import forms
from menu.models import FoodItem

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