from django import forms


class UserDataForm(forms.Form):                
    age = forms.IntegerField(min_value=1, max_value=150)
    weight = forms.FloatField(min_value=1, max_value=600)
    height = forms.FloatField(min_value=1, max_value=300)
