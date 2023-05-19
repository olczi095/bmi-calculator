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
    

class CalculatedData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bmi = models.FloatField(default=0)
    bmi_category = models.CharField(
        default='unknown',
        max_length=100
    )
    pal = models.CharField(
        default='unknown',
        max_length=100
    )
    tmr = models.FloatField(default=0)

    def __str__(self):
        return self.user.get_username()