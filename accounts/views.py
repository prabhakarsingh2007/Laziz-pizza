from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserForm()
    return render(request, 'accounts/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username, password=password)
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            return redirect('home')
        except User.DoesNotExist:
            pass
    
    form = UserForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout(request):
    request.session.flush()
    return redirect('home')