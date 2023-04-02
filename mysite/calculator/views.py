from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import UserDataForm

# Create your views here.
def home(request):
    # Redirect directly to the bmi calculator website
    return redirect('bmi')

def bmi_calculator(request):

    if request.method == 'POST':
            form = UserDataForm(request.POST)
            if form.is_valid():  
                return HttpResponseRedirect('thank you!')
    else:
        form = UserDataForm
    return render(request, 'calculator/bmi.html', {'form': form})