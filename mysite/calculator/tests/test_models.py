from django.contrib.auth.models import User
from django.test import TestCase

from calculator.models import CalculatedData, Person


class PersonTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user', password='test_password'
        )
        self.second_user = User.objects.create_user(
            username='test_second_user', password='test_second_password'
        )
        Person.objects.create(user=self.user, weight=80,
                              height=175, gender='male', age=30)
        Person.objects.create(user=self.second_user, weight=60,
                              height=160, gender='female', age=40)

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


class CalculatedDataTestCase(TestCase):

    def setUp(self):
        self.person = Person.objects.create(
            name='test_person')
        self.calculated_data = CalculatedData.objects.get(person=self.person)
        self.calculated_data.bmi = 18
        self.calculated_data.pal = '2.0'
        self.calculated_data.tmr = 2000
        self.calculated_data.save()

    def test_calculated_data_string_representation(self):
        self.assertEqual(str(self.calculated_data), 'test_person')
        self.assertTrue(isinstance(self.calculated_data, CalculatedData))

    def test_calculated_data_labels(self):
        self.assertEqual(self.calculated_data._meta.get_field(
            'bmi').verbose_name, 'bmi')
        self.assertEqual(self.calculated_data._meta.get_field(
            'bmi_category').verbose_name, 'bmi category')
        self.assertEqual(self.calculated_data._meta.get_field(
            'pal').verbose_name, 'pal')
        self.assertEqual(self.calculated_data._meta.get_field(
            'tmr').verbose_name, 'tmr')

    def test_calculated_data_with_correct_values(self):
        self.assertEqual(self.calculated_data.bmi, 18)
        self.assertEqual(self.calculated_data.bmi_category, None)
        self.assertEqual(self.calculated_data.pal, '2.0')
        self.assertEqual(self.calculated_data.tmr, 2000)

    def test_calculated_data_with_incorrect_values(self):
        self.assertNotEqual(self.calculated_data.bmi, 30)
        self.assertNotEqual(self.calculated_data.bmi_category, 'female')
        self.assertNotEqual(self.calculated_data.pal, '1.0')
        self.assertNotEqual(self.calculated_data.tmr, 1500)
