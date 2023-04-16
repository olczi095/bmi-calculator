from django import forms


class UserDataForm(forms.Form):                
    age = forms.IntegerField(required=False,label='Age ', min_value=1, max_value=150)
    weight = forms.FloatField(required=False, label='Weight    ', min_value=1, max_value=600,
                              widget=forms.NumberInput(attrs={'placeholder': 'kg ', 
                                                              'style': 'text-align: right; max-width: 70%; '
                                                              }))
    height = forms.FloatField(required=False, label='Height ', min_value=1, max_value=300, 
                              widget=forms.NumberInput(attrs={'placeholder': 'cm ',
                                                              'style': 'text-align: right; max-width: 70%'
                                                              }))
    gender = forms.ChoiceField(required=False, label='Gender ', choices = [
                                ('male', 'male'),
                                ('female', 'female')])