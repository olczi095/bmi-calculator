from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    # Redirect directly to the bmi calculator website
    return redirect('bmi')

def bmi_calculator(request):
    return render(request, 'bmicalculator/base.html')
