from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request)
        # log in the user with form
        return redirect('calculator:home')
    else:
        form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})
    