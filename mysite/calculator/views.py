from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import UserDataForm
from django.views.generic import FormView
from django.urls import reverse_lazy

def home(request):
    # Redirect directly to the bmi calculator website
    return redirect('bmi')

def bmi_calculator(request):
    if request.method == 'POST':
            form = UserDataForm(request.POST)
            if form.is_valid():  
                pass
    else:
        form = UserDataForm
    return render(request, 'calculator/bmi.html', {'form': form})
