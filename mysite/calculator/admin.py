from django.contrib import admin

from .models import CalculatedData, Person

admin.site.register(Person)


@admin.register(CalculatedData)
class CalculatedDataAdmin(admin.ModelAdmin):
    readonly_fields = ('person', 'bmi', 'bmi_category', 'bmr', 'pal', 'tmr')
