from rest_framework import permissions

from calculator.models import CalculatedData, Person


class IsOwnerOrIsAdminUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Person):
            return obj.user == request.user or request.user.is_staff
        if isinstance(obj, CalculatedData):
            return obj.person.user == request.user or request.user.is_staff
