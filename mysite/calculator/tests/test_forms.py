from django.test import TestCase
from calculator.forms import UserDataForm


class UserDataFormTest(TestCase):

    def setUp(self):
        self.form = UserDataForm()

    def test_field_placeholders(self):
        self.assertEqual(self.form.fields['weight'].widget.attrs['placeholder'], 'kg ')
        self.assertEqual(self.form.fields['height'].widget.attrs['placeholder'], 'cm ')

    def test_field_labels(self):
        self.assertEqual(self.form.fields['age'].label, 'Age ')
        self.assertEqual(self.form.fields['weight'].label, 'Weight ')
        self.assertEqual(self.form.fields['height'].label, 'Height ')
        self.assertEqual(self.form.fields['gender'].label, 'Gender ')
        self.assertEqual(self.form.fields['pal'].label, 'PAL ')

    def test_fields_existing(self):
        self.assertIn('age', self.form.fields)
        self.assertIn('weight', self.form.fields)
        self.assertIn('height', self.form.fields)
        self.assertIn('gender', self.form.fields)
        self.assertIn('pal', self.form.fields)

    def test_valid_data(self):
        form = UserDataForm(data={
            'age': 30,
            'weight': 50,
            'height': 160,
            'gender': 'female',
            'pal': 2.0
        })
        self.assertTrue(form.is_valid())

    def test_invalid_age(self):
        invalid_data = [
            {'age': -20},
            {'age': 300},
        ]
        for invalid_age in invalid_data:
            form = UserDataForm(data=invalid_age)
            self.assertFalse(form.is_valid())

    def test_invalid_weight(self):
        invalid_data = [
            {'weight': -20},
            {'weight': 1000},
        ]
        for invalid_weight in invalid_data:
            form = UserDataForm(data=invalid_weight)
            self.assertFalse(form.is_valid())

    def test_invalid_height(self):
        invalid_data = [
            {'height': -10},
            {'height': 500},
        ]
        for invalid_height in invalid_data:
            form = UserDataForm(data=invalid_height)
            self.assertFalse(form.is_valid())

    def test_invalid_gender(self):
        invalid_data = [
            {'gender': 'parrot'},
            {'gender': 'elephant'},
        ]
        for invalid_gender in invalid_data:
            form = UserDataForm(data=invalid_gender)
            self.assertFalse(form.is_valid())

    def test_invalid_pal(self):
        invalid_data = [
            {'pal': -2.0},
            {'pal': 4.0},
        ]
        for invalid_pal in invalid_data:
            form = UserDataForm(data=invalid_pal)
            self.assertFalse(form.is_valid())