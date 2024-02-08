from django.contrib import admin
from .models import Person, CalculatedData

admin.site.register(Person)
admin.site.register(CalculatedData)