from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    weight = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    gender = models.CharField(
        default='unknown',
        max_length=100
    )
    age = models.IntegerField(default=0)

    def __str__(self):
        return self.user.get_username()

    def update_or_create_data(self, new_data):
        self.weight = new_data.get('weight', self.weight)
        self.height = new_data.get('height', self.height)
        self.gender = new_data.get('gender', self.gender)
        self.age = new_data.get('age', self.age)
        self.save()


class CalculatedData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bmi = models.FloatField(default=0)
    bmi_category = models.CharField(
        default='unknown',
        max_length=100
    )
    bmr = models.FloatField(default=0)
    pal = models.CharField(
        default='unknown',
        max_length=100
    )
    tmr = models.FloatField(default=0)

    def __str__(self):
        return self.user.get_username()

    def update_or_create_data(self, new_data):
        self.bmi = new_data.get('bmi', self.bmi)
        self.bmi_category = new_data.get('bmi_category', self.bmi_category)
        self.bmr = new_data.get('bmr', self.bmr)
        self.pal = new_data.get('pal', self.pal)
        self.tmr = new_data.get('tmr', self.tmr)
        self.save()
