from django.shortcuts import render, get_object_or_404
from .models import FoodItem

# Create your views here.

def menu(request):
    food_items = FoodItem.objects.all()
    return render(request, 'menu/menu.html', {'food_items': food_items})

def food_detail(request, food_id):
    food = get_object_or_404(FoodItem, id=food_id)
    return render(request, 'menu/food_detail.html', {'food': food})
