from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from calculator.models import Person

from .serializers import PersonSerializer


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.exclude(user__is_active=False)
    serializer_class = PersonSerializer
    permission_classes = [IsAdminUser]
