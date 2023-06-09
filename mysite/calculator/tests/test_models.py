from django.forms import ValidationError
from django.test import TestCase
from calculator.models import Person
from django.contrib.auth.models import User


class PersonTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.second_user = User.objects.create_user(username='test_second_user', password='test_second_password')
        Person.objects.create(user=self.user, weight=80, height=175, gender='male', age=30)
        Person.objects.create(user=self.second_user, weight=60, height=160, gender='female', age=40)

    def test_person_string_representation(self):
        person = Person.objects.get(id=2)
        self.assertEqual(str(person), 'test_second_user')
        self.assertTrue(isinstance(person, Person))
    
    def test_person_labels(self):
        person = Person.objects.get(id=1)
        self.assertEqual(person._meta.get_field('weight').verbose_name, 'weight')
        self.assertEqual(person._meta.get_field('height').verbose_name, 'height')
        self.assertEqual(person._meta.get_field('gender').verbose_name, 'gender')
        self.assertEqual(person._meta.get_field('age').verbose_name, 'age')

    def test_person_with_correct_values(self):
        person = Person.objects.get(id=1)
        self.assertEqual(person.weight, 80)
        self.assertEqual(person.height, 175)
        self.assertEqual(person.gender, 'male')
        self.assertEqual(person.age, 30)

    def test_person_with_incorrect_values(self):
        person = Person.objects.get(id=1)
        self.assertNotEqual(person.weight, 100)
        self.assertNotEqual(person.height, 200)
        self.assertNotEqual(person.gender, 'female')
        self.assertNotEqual(person.age, 60)
