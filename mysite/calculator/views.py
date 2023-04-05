from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserDataForm
from django.views.generic import FormView

def home(request):
    # Redirect directly to the bmi calculator website
    return redirect('bmi')


class BmiFormView(FormView):
     form_class = UserDataForm
     template_name = 'calculator/bmi.html'
