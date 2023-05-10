from django.db import models
from django.contrib.auth.models import User


class LoggedInUser(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
        )
    weight = models.IntegerField()
    height = models.IntegerField()
    gender = models.CharField(
        max_length=100
        )
    pal = models.CharField(
        max_length=100
        )
