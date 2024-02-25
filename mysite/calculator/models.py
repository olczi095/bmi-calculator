from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Gender(models.TextChoices):
    MALE = 'male', _('male'),
    FEMALE = 'female', _('female'),


class PALValue(models.TextChoices):
    ONE_TWO = '1.2', '1.2'
    ONE_THREE = '1.3', '1.3'
    ONE_FOUR = '1.4', '1.4'
    ONE_FIVE = '1.5', '1.5'
    ONE_SIX = '1.6', '1.6'
    ONE_SEVEN = '1.7', '1.7'
    ONE_EIGHT = '1.8', '1.8'
    ONE_NINE = '1.9', '1.9'
    TWO_ZERO = '2.0', '2.0'
    TWO_TWO = '2.2', '2.2'


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50)
    weight = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    gender = models.CharField(choices=Gender.choices,
                              max_length=8, null=True, blank=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    pal = models.CharField(choices=PALValue.choices, default='1.2',
                           max_length=3, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.user:
            if self.user.first_name and self.user.last_name:
                self.name = f"{self.user.first_name} {self.user.last_name}"
            else:
                self.name = self.user.username

        return super().save(*args, **kwargs)

    def update_or_create_data(self, new_data):
        self.weight = new_data.get('weight', self.weight)
        self.height = new_data.get('height', self.height)
        self.gender = new_data.get('gender', self.gender)
        self.age = new_data.get('age', self.age)
        self.pal = new_data.get('pal', self.pal)
        self.save()


class CalculatedData(models.Model):
    person = models.OneToOneField(
        Person, on_delete=models.CASCADE, related_name='calculated_data'
    )
    bmi = models.FloatField(null=True)
    bmi_category = models.CharField(
        null=True, max_length=100
    )
    bmr = models.FloatField(null=True)
    pal = models.CharField(
        choices=PALValue.choices, default='1.2', max_length=3, blank=True, null=True
    )
    tmr = models.FloatField(null=True)

    def __str__(self):
        return self.person.name

    def update_or_create_data(self, new_data):
        self.bmi = new_data.get('bmi', self.bmi)
        self.bmi_category = new_data.get('bmi_category', self.bmi_category)
        self.bmr = new_data.get('bmr', self.bmr)
        self.pal = new_data.get('pal', self.pal)
        self.tmr = new_data.get('tmr', self.tmr)
        self.save()
