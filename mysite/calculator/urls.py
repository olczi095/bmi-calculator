from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('bmi_calculator/', views.bmi_calculator , name='bmi'),
]
