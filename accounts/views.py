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
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
            from django.contrib.auth.hashers import check_password
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                request.session['name'] = user.name
                return redirect('home')
            else:
                error = "Invalid username or password"
        except User.DoesNotExist:
            error = "Invalid username or password"
    
    return render(request, 'accounts/login.html', {'error': error})

def logout(request):
    request.session.flush()
    return redirect('home')