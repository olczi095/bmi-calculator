from django import forms


class UserDataForm(forms.Form):                
    age = forms.IntegerField(label='Age ', min_value=1, max_value=150)
    weight = forms.FloatField(label='Weight    ', min_value=1, max_value=600,
                              widget=forms.NumberInput(attrs={'placeholder': 'kg ', 
                                                              'style': 'text-align: right; max-width: 70%; '
                                                              }))
    height = forms.FloatField(label='Height ', min_value=1, max_value=300, 
                              widget=forms.NumberInput(attrs={'placeholder': 'cm ',
                                                              'style': 'text-align: right; max-width: 70%'
                                                              }))
    gender = forms.ChoiceField(label='Gender ', choices = [
                                ('male', 'male'),
                                ('female', 'female')])