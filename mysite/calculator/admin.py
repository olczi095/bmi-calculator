from django.contrib import admin
from django.db.models.functions import Lower
from django.urls import reverse
from django.utils.html import format_html

from .models import CalculatedData, Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'user', 'calculated_data_link')
        }),
        ('Biometric Data', {
            'fields': ('weight', 'height', 'gender', 'age', 'pal')
        }),
    )
    readonly_fields = ('calculated_data_link',)
    list_display = ('name', 'age', 'gender', 'user_link', 'calculated_data_link')
    list_filter = ('user__is_active', 'gender')
    search_fields = ('name', 'user__username')
    ordering = (Lower('name'),)

    def user_link(self, obj):
        """Generate a link to the related user in the admin panel."""
        if obj.user:
            user_admin_path = reverse(
                'admin:auth_user_change',
                args=(obj.user.pk,)
            )
            return format_html(
                f'<a href="{user_admin_path}">{obj.user}</a>'
            )
        else:
            return None
    user_link.short_description = 'user'

    def calculated_data_link(self, obj):
        """Generate a link to the related calculated data in the admin panel."""
        if obj.calculated_data:
            calculateddata_admin_path = reverse(
                'admin:calculator_calculateddata_change',
                args=(obj.calculated_data.pk,)
            )
            return format_html(
                f'<a href="{calculateddata_admin_path}">{obj.calculated_data}</a>'
            )
        else:
            return None
    calculated_data_link.short_description = 'calculated data'


@admin.register(CalculatedData)
class CalculatedDataAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('person',)
        }),
        ('Calculated Data', {
            'fields': ('bmi', 'bmi_category', 'bmr', 'pal', 'tmr')
        }),
    )
    readonly_fields = ('person', 'bmi', 'bmi_category', 'bmr', 'pal', 'tmr')
    list_display = ('person', 'bmi', 'bmi_category')
    list_filter = ('person__user__is_active', 'bmi_category')
    search_fields = ('person__name',)

    ordering = (Lower('person__name'),)
