from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from calculator.views import home as home_page


class SignUpTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = Client()
        cls.login_url = reverse('accounts:login')
        cls.logout_url = reverse(home_page)
        cls.valid_data = {
            'username': 'testuser',
            'email': 'testuser@test.com', 
            'password1': 'testpassword',
            'password2': 'testpassword'}
        super().setUpClass()
                  
    def test_display_registration_view(self):
        response = self.client.get(reverse('accounts:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')
        
        
    def test_redirect_after_valid_sign_up(self):
        response = self.client.post(reverse('accounts:signup'), self.valid_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calculator/bmi.html')
        user = User.objects.get(username='testuser')
        self.assertTrue(user.is_authenticated)


    def test_signup_view_post_invalid_form(self):
        response = self.client.post(reverse('accounts:signup'), {'username': 'testuser', 
                                                                 'email': 'testuser@mail.com',
                                                                 'password1': 'testpassword', 
                                                                 'password2': 'invalidtestpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')
        self.assertFalse(response.context['form'].is_valid())

    def test_login(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword'
        }, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.logout_url, follow=True)
        self.assertEqual(response.status_code, 200)