from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class BMICalculationAPITest(APITestCase):
    def setUp(self):
        self.path = reverse('bmi-calculation')
        self.data = {
            "height": 170,
            "weight": 70
        }

    def test_get_method_not_allowed(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_method_with_valid_data(self):
        response = self.client.post(self.path, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_fields = ['bmi', 'bmi_category', 'description', 'message']
        for expected_field in expected_fields:
            self.assertIn(expected_field, response.data)

    def test_bmi_calculation(self):
        expected_bmi = 24.22
        expected_bmi_category = 'normal weight'

        response = self.client.post(self.path, data=self.data)
        self.assertEqual(response.data['bmi'], expected_bmi)
        self.assertEqual(response.data['bmi_category'], expected_bmi_category)
        self.assertEqual(response.data['message'], 'BMI calculated successfully')

    # Tests with invalid data
    def test_post_method_without_data(self):
        data = {}
        response = self.client.post(self.path, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        for field in response.data:
            self.assertEqual('This field is required.', response.data[field][0])

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


class TMRCalculationAPITest(APITestCase):
    def setUp(self):
        self.path = reverse('tmr-calculation')
        self.data = {
            "age": 30,
            "gender": "male",
            "height": 170,
            "weight": 70,
            "pal": "1.2"
        }

    def test_get_method_not_allowed(self):
        response = self.client.get(self.path, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # Tests with valid data
    def test_post_method_for_male_data(self):
        response = self.client.post(self.path, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tmr', response.data)
        self.assertIn('message', response.data)

    def test_post_method_for_female_data(self):
        self.data['gender'] = 'female'
        response = self.client.post(self.path, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tmr', response.data)
        self.assertIn('message', response.data)

    def test_tmr_calculation_for_male(self):
        expected_tmr = 1941.0

        response = self.client.post(self.path, data=self.data)
        self.assertEqual(response.data['tmr'], expected_tmr)
        self.assertEqual(response.data['message'], 'TMR calculated successfully')

    def test_tmr_calculation_for_female(self):
        self.data['gender'] = 'female'
        expected_tmr = 1741.8

        response = self.client.post(self.path, data=self.data)
        self.assertEqual(response.data['tmr'], expected_tmr)
        self.assertEqual(response.data['message'], 'TMR calculated successfully')

    # Tests with invalid data
    def test_post_method_without_data(self):
        self.data = {}
        response = self.client.post(self.path, data=self.data)
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

    def test_post_method_with_invalid_pal(self):
        self.data['pal'] = '3.0'
        response = self.client.post(self.path, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('is not a valid choice', response.data['pal'][0])

    def test_post_method_with_no_pal(self):
        self.data['pal'] = ''
        response = self.client.post(self.path, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('is not a valid choice', response.data['pal'][0])
