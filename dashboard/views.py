from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import User
from menu.models import FoodItem, Category
from orders.models import Order
from reservation.models import Reservation
from .forms import FoodForm


# ================= Dashboard =================

def dashboard(request):

    context = {
        "total_users": User.objects.count(),
        "total_foods": FoodItem.objects.count(),
        "total_orders": Order.objects.count(),
        "total_reservations": Reservation.objects.count(),
        "recent_orders": Order.objects.all().order_by("-id")[:5],
        "recent_reservations": Reservation.objects.all().order_by("-id")[:5],
    }

    return render(request, "dashboard/dashboard.html", context)


# ================= Food List =================

def food_list(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    food_type = request.GET.get('food_type', '')
    
    foods = FoodItem.objects.all().order_by("-id")
    
    if query:
        foods = foods.filter(name__icontains=query)
    if category:
        foods = foods.filter(category__name=category)
    if food_type:
        foods = foods.filter(food_type=food_type)
        
    categories = Category.objects.all().order_by('name')

    context = {
        "foods": foods,
        "categories": categories,
        "selected_category": category,
        "selected_food_type": food_type,
        "search_query": query,
    }

    return render(request, "dashboard/foods.html", context)


# ================= Add Food =================

def add_food(request):

    if request.method == "POST":

        form = FoodForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("food_list")

    else:
        form = FoodForm()

    return render(request, "dashboard/add_food.html", {
        "form": form
    })


# ================= Edit Food =================

def edit_food(request, id):

    food = get_object_or_404(FoodItem, id=id)

    if request.method == "POST":

        form = FoodForm(request.POST, request.FILES, instance=food)

        if form.is_valid():
            form.save()
            return redirect("food_list")

    else:
        form = FoodForm(instance=food)

    return render(request, "dashboard/edit_food.html", {
        "form": form,
        "food": food,
    })


# ================= Delete Food =================

def delete_food(request, id):

    food = get_object_or_404(FoodItem, id=id)

    if request.method == "POST":
        food.delete()
        return redirect("food_list")

    return render(request, "dashboard/delete_food.html", {
        "food": food,
    })


# ================= Manage Orders =================

def admin_orders(request):
    orders = Order.objects.all().order_by("-id")
    return render(request, "dashboard/orders.html", {"orders": orders})


# ================= Manage Reservations =================

def admin_reservations(request):
    reservations = Reservation.objects.all().order_by("-id")
    return render(request, "dashboard/reservations.html", {"reservations": reservations})


# ================= Manage Users =================

def admin_users(request):
    users = User.objects.all().order_by("-id")
    return render(request, "dashboard/users.html", {"users": users})






# ================= Order Detail =================

def order_detail(request, id):

    order = get_object_or_404(Order, id=id)

    return render(request, "dashboard/order_detail.html", {
        "order": order
    })


# ================= Update Order Status =================

def update_order_status(request, id):

    order = get_object_or_404(Order, id=id)

    if request.method == "POST":

        order.status = request.POST.get("status")
        order.save()

        return redirect("admin_orders")

    return redirect("order_detail", id=id)


def sales(request):

    total_orders = Order.objects.count()
    total_sales = sum(order.total_price for order in Order.objects.all())

    context = {
        "total_orders": total_orders,
        "total_sales": total_sales,
        "orders": Order.objects.all().order_by("-id"),
    }

    return render(request, "dashboard/sales.html", context)


# ================= Manage Categories =================

def category_list(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Category.objects.get_or_create(name=name)
            return redirect("category_list")

    categories = Category.objects.all().order_by("name")
    return render(request, "dashboard/categories.html", {"categories": categories})


def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == "POST":
        category.delete()
        return redirect("category_list")
    return render(request, "dashboard/delete_category.html", {"category": category})