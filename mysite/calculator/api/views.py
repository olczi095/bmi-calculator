from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from calculator.models import Person

from .permissions import IsOwnerOrIsAdminUser
from .serializers import PersonSerializer


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.exclude(user__is_active=False)
    serializer_class = PersonSerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.action in ('retrieve', 'update', 'partial_update'):
            self.permission_classes = [IsOwnerOrIsAdminUser]
        return super().get_permissions()
