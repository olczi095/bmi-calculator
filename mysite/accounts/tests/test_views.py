from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class SignUpTestCase(TestCase):

    valid_data = {'username': 'monika123',
                  'email': 'monika@mail.com', 
                  'password1': 'mojeHaslo1.',
                  'password2': 'mojeHaslo1.'}
                  
    def test_display_registration_view(self):
        response = self.client.get(reverse('accounts:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')
        
        
    def test_redirect_after_valid_sign_up(self):
        response = self.client.post(reverse('accounts:signup'), self.valid_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calculator/bmi.html')
        user = User.objects.get(username='monika123')
        self.assertTrue(user.is_authenticated)


    def test_signup_view_post_invalid_form(self):
        response = self.client.post(reverse('accounts:signup'), {'username': 'testuser', 
                                                                 'email': 'testuser@mail.com',
                                                                 'password1': 'correctpass', 
                                                                 'password2': 'notcorrectpas'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')
        self.assertFalse(response.context['form'].is_valid())
