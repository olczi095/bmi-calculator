from accounts.forms import RegisterForm
from django.test import TestCase


class RegisterFormTestCase(TestCase):
    
    def setUp(self):
        self.form = RegisterForm()

    def test_valid_form(self):
        form_data = {
            'username': 'adam123',
            'email': 'adam@gmail.com',
            'password1': 'Ziemniak1',
            'password2': 'Ziemniak1'
        }
        register_user = RegisterForm(data=form_data)
        self.assertTrue(register_user.is_valid())

    def test_invalid_form_with_two_different_passwords(self):
        form_data = {
            'username': 'adam123',
            'email': 'adam@gmail.com',
            'password1': 'Ziemniak2',
            'password2': 'Ziemniak1'
        }
        register_user = RegisterForm(data=form_data)
        self.assertFalse(register_user.is_valid())
        self.assertEqual(register_user.errors['password2'][0], 'The two password fields didn’t match.')        

    def test_invalid_form_without_email(self):
        data_form = {
            'username': 'adam123',
            'password1': 'Ziemniak1',
            'password2': 'Ziemniak1'
        }
        form = RegisterForm(data=data_form)
        self.assertFalse(form.is_valid())

    def test_existing_fields(self):
        self.assertIn('username', self.form.fields)
        self.assertIn('email', self.form.fields)
        self.assertIn('password1', self.form.fields)
        self.assertIn('password2', self.form.fields)
