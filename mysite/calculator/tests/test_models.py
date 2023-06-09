from django.test import TestCase
from calculator.models import Person
from django.contrib.auth.models import User


class PersonTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        Person.objects.create(user=self.user, weight=80, height=175, gender='male', age=30)

    def test_weight_label(self):
        person = Person.objects.get(id=1)
        weight_field_label = person._meta.get_field('weight').verbose_name
        self.assertEqual(weight_field_label, 'weight')

    def test_weight_value(self):
        person = Person.objects.get(id=1)
        person_weight = person.weight
        expected_weight = 80
        self.assertEqual(person_weight, expected_weight)

    def test_height_label(self):
        person = Person.objects.get(id=1)
        height_field_label = person._meta.get_field('height').verbose_name
        self.assertEqual(height_field_label, 'height')

    def test_height_value(self):
        person = Person.objects.get(id=1)
        person_height = person.height
        expected_height = 175
        self.assertEqual(person_height, expected_height)

    def test_gender_label(self):
        person = Person.objects.get(id=1)
        gender_field_label = person._meta.get_field('gender').verbose_name
        self.assertEqual(gender_field_label, 'gender')

    def test_gender_value(self):
        person = Person.objects.get(id=1)
        person_gender = person.gender
        expected_gender = 'male'
        self.assertEqual(person_gender, expected_gender)

    def test_age_label(self):
        person = Person.objects.get(id=1)
        age_field_label = person._meta.get_field('age').verbose_name
        self.assertEqual(age_field_label, 'age')

    def test_age_value(self):
        person = Person.objects.get(id=1)
        person_age = person.age
        expected_value = 30
        self.assertEqual(person_age, expected_value)
