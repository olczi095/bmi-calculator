from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('bmi_calculator/', views.bmi_calculator , name='bmi'),
    path('bmi_calculator/filled/', views.bmi_calculator_filled_out, name='bmi-filled'),
    path('bmr_calculator/', views.bmr_calculator, name='bmr'),
    path('bmr_calculator/filled/', views.bmr_calculator_filled_out, name='bmr-filled'),
    path('pal_calculator/', views.pal_calculator, name='pal'),
    path('tmr_calculator/', views.tmr_calculator, name='tmr'),
    path('tmr_calculator/filled/', views.tmr_calculator_filled_out, name='tmr-filled'),
]
