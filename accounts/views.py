from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            from django.contrib import messages
            messages.success(request, "Account created successfully! Please login.")
            return redirect('login')
        else:
            from django.contrib import messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').capitalize()}: {error}")
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

def profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = User.objects.get(id=user_id)
    return render(request, 'accounts/profile.html', {'user': user})