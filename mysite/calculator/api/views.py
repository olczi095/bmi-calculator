from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from calculator.models import CalculatedData, Person
from calculator.views import checking_bmi_category

from .permissions import IsOwnerOrIsAdminUser
from .serializers import CalculatedDataSerializer, PersonSerializer


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.exclude(user__is_active=False)
    serializer_class = PersonSerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.action in ('retrieve', 'update', 'partial_update'):
            self.permission_classes = [IsOwnerOrIsAdminUser]
        return super().get_permissions()


class CalculatedDataListView(generics.ListAPIView):
    queryset = CalculatedData.objects.exclude(person__user__is_active=False)
    serializer_class = CalculatedDataSerializer
    permission_classes = [IsAdminUser]


class CalculatedDataDetailView(generics.RetrieveDestroyAPIView):
    queryset = CalculatedData.objects.exclude(person__user__is_active=False)
    serializer_class = CalculatedDataSerializer
    permission_classes = [IsOwnerOrIsAdminUser]


class CalculateBMIAPIView(APIView):
    """
    A view to calculate BMI (Body Mass Index) for any user.

    Usage:
        1. Use POST method to  calculate BMI.
        2. Required input data: weight (in kilograms) and height (in centimeters)

    Sample request data:
        {
            "weight": 70,
            "height": 170
        }
    """

    name = "BMI Calculation API"

    def get(self, request):
        return Response(
            {'message': 'Please use POST method to calculate BMI.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def post(self, request):
        """
        Calculate BMI based on provided height (centimeters) and weight (kilograms).
        """
        height = float(request.data.get('height', 0))
        weight = float(request.data.get('weight', 0))

        if 300 > height > 0 and 600 > weight > 0:
            bmi = round(weight / (height * 0.01) ** 2, 2)
            bmi_category = checking_bmi_category(bmi)
            description = bmi_category['description']
            return Response(
                {'bmi': bmi, 'bmi_category': bmi_category['category'],
                    'description': description},
                status=status.HTTP_200_OK)
        else:
            return Response(
                {'message': 'Invalid data. Please provide valid height and weight.'},
                status.HTTP_400_BAD_REQUEST
            )
