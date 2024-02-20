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

    def test_post_method_with_valid_data(self):
        data = {"height": 170.0, "weight": 70.5}
        response = self.client.post(self.path, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_method_with_invalid_data(self):
        data = {"height": -170, "weight": 70}
        response = self.client.post(self.path, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BMRCalculationAPITest(APITestCase):
    def setUp(self):
        self.path = reverse('bmr-calculation')
        self.data = {
            "age": 30,
            "gender": "male",
            "height": 170,
            "weight": 70
        }

    # Tests with valid data
    def test_get_method_not_allowed(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_method_for_female_data(self):
        response = self.client.post(self.path, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('bmr', response.data)
        self.assertIn('message', response.data)

    def test_post_method_for_male_data(self):
        self.data['gender'] = 'female'
        response = self.client.post(self.path, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('bmr', response.data)
        self.assertIn('message', response.data)

    def test_bmr_calculation_for_male(self):
        expected_bmr = 1617.5

        response = self.client.post(self.path, data=self.data)
        self.assertEqual(response.data['bmr'], expected_bmr)
        self.assertEqual(response.data['message'], 'BMR calculated successfully')

    def test_bmr_calculation_for_female(self):
        self.data['gender'] = 'female'
        expected_bmr = 1451.5

        response = self.client.post(self.path, data=self.data)
        self.assertEqual(response.data['bmr'], expected_bmr)
        self.assertEqual(response.data['message'], 'BMR calculated successfully')

    # Tests with invalid data
    def test_post_method_without_data(self):
        data = {}
        response = self.client.post(self.path, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        for field in response.data:
            self.assertEqual('This field is required.', response.data[field][0])

    def test_post_method_with_negative_age(self):
        self.data['age'] = -30
        response = self.client.post(self.path, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('Age must be a positive integer', response.data['age'][0])

    def test_post_method_with_invalid_gender(self):
        self.data['gender'] = 'other'
        response = self.client.post(self.path, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('is not a valid choice', response.data['gender'][0])

    def test_post_method_with_no_gender(self):
        self.data['gender'] = ''
        response = self.client.post(self.path, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('is not a valid choice', response.data['gender'][0])

    def test_post_method_with_negative_height(self):
        self.data['height'] = -170
        response = self.client.post(self.path, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('Height must be greater than 0', response.data['height'][0])

    def test_post_method_with_height_greater_than_300(self):
        self.data['height'] = 310
        response = self.client.post(self.path, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('Height must be less than 300', response.data['height'][0])

    def test_post_method_with_negative_weight(self):
        self.data['weight'] = -70
        response = self.client.post(self.path, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('Weight must be greater than 0', response.data['weight'][0])

    def test_post_method_with_weight_greater_than_1000(self):
        self.data['weight'] = 1100
        response = self.client.post(self.path, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('Weight must be less than 1000', response.data['weight'][0])
