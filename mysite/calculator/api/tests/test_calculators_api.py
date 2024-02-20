from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class BMICalculationAPITest(APITestCase):
    def setUp(self):
        self.path = reverse('bmi-calculation')

    def test_get_method_not_allowed(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_method_valid_data(self):
        data = {"height": 170, "weight": 70}
        response = self.client.post(self.path, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('bmi', response.data)
        self.assertIn('bmi_category', response.data)
        self.assertIn('description', response.data)

    def test_post_method_valid_float_data(self):
        data = {"height": 170.0, "weight": 70.5}
        response = self.client.post(self.path, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_method_invalid_data(self):
        data = {"height": -170, "weight": 70}
        response = self.client.post(self.path, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
