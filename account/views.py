# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import CustomAuthenticationForm
from order.models import Order

def login_view(request):
    if request.user.is_authenticated:
        return redirect('account:dashboard')  # Redirect if already logged in

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('account:dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'account/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('account:login')  # or another URL like home

def dashboard(request):
    order_list = Order.objects.all()

    context = {'order_list': order_list}
    return render(request, 'account/dashboard.html', context)