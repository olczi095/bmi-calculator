from django import forms


class UserDataForm(forms.Form):
    gender = forms.ChoiceField(choices=[
        ("male", "♂︎ Male"),
        ("female", "♀︎ Female")
    ])                     
    age = forms.IntegerField(min_value=1, max_value=150)
    weight = forms.FloatField(min_value=1)
    height = forms.FloatField(min_value=1)
