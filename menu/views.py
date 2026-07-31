from django.shortcuts import render, get_object_or_404
from .models import FoodItem, Category

def menu(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    # 'type' ya 'food_type' dono parameters se data handle hoga
    food_type = request.GET.get('type') or request.GET.get('food_type', '')
    
    food_items = FoodItem.objects.filter(available=True).select_related('category')
    
    # 1. Search Query Filter
    if query:
        food_items = food_items.filter(name__icontains=query)
        
    # 2. Category Filter (Supports both Category ID and Category Name)
    if category:
        if category.isdigit():
            food_items = food_items.filter(category__id=int(category))
        else:
            food_items = food_items.filter(category__name__iexact=category)
            
    # 3. Veg / Non-Veg Filter
    if food_type in ['Veg', 'Non-Veg']:
        food_items = food_items.filter(food_type=food_type)
        
    categories = Category.objects.all().order_by('name')
    
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
    # Related items derived from same category
    related_foods = FoodItem.objects.filter(category=food.category, available=True).exclude(id=food.id)[:4]
    
    context = {
        'food_item': food,
        'related_foods': related_foods,
    }
    return render(request, 'menu/food_detail.html', context)