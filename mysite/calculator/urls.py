from django.urls import path
from .views import BmiFormView
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('bmi_calculator/', BmiFormView.as_view(), name='bmi'),
]