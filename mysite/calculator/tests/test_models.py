from django.test import TestCase
from calculator.models import Person
from django.contrib.auth.models import User


class PersonTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test_user', password='test_password')
        Person.objects.create(user=cls.user, weight=80, height=175, gender='male', age=30)

    def setUp(self):
        self.person = Person.objects.get(id=1)

    def test_weight_label(self):
        weight_field_label = self.person._meta.get_field('weight').verbose_name
        self.assertEqual(weight_field_label, 'weight')

    def test_weight_value(self):
        person_weight = self.person.weight
        expected_weight = 80
        self.assertEqual(person_weight, expected_weight)

    def test_height_label(self):
        height_field_label = self.person._meta.get_field('height').verbose_name
        self.assertEqual(height_field_label, 'height')

    def test_height_value(self):
        person_height = self.person.height
        expected_height = 175
        self.assertEqual(person_height, expected_height)

    def test_gender_label(self):
        gender_field_label = self.person._meta.get_field('gender').verbose_name
        self.assertEqual(gender_field_label, 'gender')

    def test_gender_value(self):
        person_gender = self.person.gender
        expected_gender = 'male'
        self.assertEqual(person_gender, expected_gender)

    def test_age_label(self):
        age_field_label = self.person._meta.get_field('age').verbose_name
        self.assertEqual(age_field_label, 'age')

    def test_age_value(self):
        person_age = self.person.age
        expected_value = 30
        self.assertEqual(person_age, expected_value)
