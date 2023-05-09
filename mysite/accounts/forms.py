from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):

    email = forms.EmailField(required=True)
    username = forms.CharField(help_text=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']