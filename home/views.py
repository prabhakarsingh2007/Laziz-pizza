from django.shortcuts import render
from home.models import PopularItem
from menu.models import FoodItem

# Create your views here.


def index(request):
    popular_items = PopularItem.objects.filter(is_active=True).select_related('category').order_by('order')
    food_items = FoodItem.objects.filter(available=True).select_related('category').order_by('-id')[:6]
    has_more_foods = FoodItem.objects.filter(available=True).count() > 6
    
    return render(request, "home/index.html", {
        'popular_items': popular_items,
        'food_items': food_items,
        'has_more_foods': has_more_foods,
    })

def about(request):
    return render(request, "home/about.html")

def contact(request):
    return render(request, "home/contact.html")


