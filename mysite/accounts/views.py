from .forms import RegisterForm
from calculator.views import home as home_page
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout

def signup_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(home_page)
    else:
        form = RegisterForm()

    context = {'form': form}
    return render(request, 'accounts/signup.html', context)
    
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(home_page)
        else:
            messages.error(request, 'The email or the password is not correct.')
            return redirect('accounts:login')
    else:
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect(home_page)