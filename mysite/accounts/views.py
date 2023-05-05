from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from calculator.views import home as home_page

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request)
        # log in the user with form
        return redirect(home_page)
    else:
        form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})
    
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(home_page)
        else:
            messages.error(request, 'The email or the password is not correct.')
            return redirect('login')
    else:
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})
