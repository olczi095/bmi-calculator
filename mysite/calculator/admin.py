from django.contrib import admin
from .models import Person, CalculatedData


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    readonly_fields = ('user',)


@admin.register(CalculatedData)
class CalculatedDataAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'bmi', 'bmi_category', 'bmr', 'pal', 'tmr')
