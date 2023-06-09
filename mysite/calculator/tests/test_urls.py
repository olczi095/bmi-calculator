from django.test import TestCase
from django.urls import reverse

class URLSTestCase(TestCase):

    def test_home_url_returns_redirect(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/bmi_calculator/')
    
    def test_bmi_returns_success(self):
        response = self.client.get(reverse('bmi'))
        self.assertEqual(response.status_code, 200)

    def test_bmi_filled_returns_redirect(self):
        response = self.client.get(reverse('bmi-filled'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/bmi_calculator/')

    def test_bmr_returns_success(self):
        response = self.client.get(reverse('bmr'))
        self.assertEqual(response.status_code, 200)

    def test_bmr_filled_returns_redirect(self):
        response = self.client.get(reverse('bmr-filled'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/bmr_calculator/')
    
    def test_pal_returns_success(self):
        response = self.client.get(reverse('pal'))
        self.assertEqual(response.status_code, 200)

    def test_tmr_returns_success(self):
        response = self.client.get(reverse('tmr'))
        self.assertEqual(response.status_code, 200)

    def test_tmr_filled_returns_redirect(self):
        response = self.client.get(reverse('tmr-filled'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/tmr_calculator/')
