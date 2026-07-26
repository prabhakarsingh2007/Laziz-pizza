from django.shortcuts import render, get_object_or_404
from .models import FoodItem

# Create your views here.

def menu(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    food_type = request.GET.get('food_type', '')
    
    food_items = FoodItem.objects.filter(available=True)
    
    if query:
        food_items = food_items.filter(name__icontains=query)
    if category:
        food_items = food_items.filter(category=category)
    if food_type:
        food_items = food_items.filter(food_type=food_type)
        
    categories = [choice[0] for choice in FoodItem.CATEGORY]
    
    context = {
        'food_items': food_items,
        'categories': categories,
        'selected_category': category,
        'selected_food_type': food_type,
        'search_query': query,
    }
    return render(request, 'menu/menu.html', context)

def food_detail(request, food_id):
    food = get_object_or_404(FoodItem, id=food_id)
    return render(request, 'menu/food_detail.html', {'food': food})
