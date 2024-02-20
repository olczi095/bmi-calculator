from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from calculator.models import CalculatedData, Person
from calculator.views import checking_bmi_category

from .permissions import IsOwnerOrIsAdminUser
from .serializers import (BMISerializer, BMRSerializer, CalculatedDataSerializer,
                          PersonSerializer)


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
            "height": 170
            "weight": 70,
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
        Calculate BMI based on provided data:
            height (centimeters),
            weight (kilograms).
        """
        serializer = BMISerializer(data=request.data)
        if serializer.is_valid():
            height = serializer.validated_data['height']
            weight = serializer.validated_data['weight']

            bmi_result = round(weight / (height * 0.01) ** 2, 2)
            bmi_category = checking_bmi_category(bmi_result)
            description = bmi_category['description']

            return Response(
                {'bmi': bmi_result, 'bmi_category': bmi_category['category'],
                 'description': description, 'message': 'BMI calculated successfully'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class CalculateBMRAPIView(APIView):
    """
    A view to calculate BMR (Basal Metabolic Rate).
    Available for any user.

    Usage:
        1. Use POST method to calculate BMR.
        2. Required input data:
            - age
            - gender ('male' or 'female')
            - height (in centimeters)
            - weight (in kilograms)

    Sample request data:
        {
            "age": 30,
            "gender": "male",
            "height": 170,
            "weight": 70
        }
    """

    name = "BMR Calculation API"

    def get(self, request):
        return Response(
            {'message': 'Please use POST method to calculate BMR.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def post(self, request):
        """
        Calculate BMR based on provided data:
            age,
            gender ('female' or 'male'),
            height (in centimeters),
            weight (in kilograms).
        """
        serializer = BMRSerializer(data=request.data)
        if serializer.is_valid():
            age = serializer.validated_data['age']
            gender = serializer.validated_data['gender']
            height = serializer.validated_data['height']
            weight = serializer.validated_data['weight']

            if gender == 'male':
                bmr_result = (10 * weight) + (6.25 * height) - (5 * age) + 5
            else:
                bmr_result = (10 * weight) + (6.25 * height) - (5 * age) - 161

            return Response(
                {'bmr': bmr_result, 'message': 'BMR calculated successfully'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
