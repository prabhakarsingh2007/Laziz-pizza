from django.shortcuts import render
from .models import PopularItem

# Create your views here.


def index(request):
    popular_items = PopularItem.objects.filter(is_active=True).order_by('order')
    return render(request, "home/index.html", {'popular_items': popular_items})

def about(request):
    return render(request, "home/about.html")

def contact(request):
    return render(request, "home/contact.html")


