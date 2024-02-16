from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from calculator.models import Person

User = get_user_model()


class PersonAPITest(APITestCase):
    @classmethod
    def setUpTestData(self):
        self.admin = User.objects.create_superuser(
            username='test_admin',
            password='test_admin_password'
        )
        self.admin_token = AccessToken.for_user(self.admin)

        self.owner = User.objects.create_user(
            username='test_owner',
            password='test_owner_password'
        )
        self.owner_token = AccessToken.for_user(self.owner)

        self.user = User.objects.create_user(
            username='test_user',
            password='test_user_password'
        )
        self.user_token = AccessToken.for_user(self.user)

        self.person1 = Person.objects.create(
            name='person1'
        )
        self.person2 = Person.objects.create(
            user=self.owner,
            name='person2'
        )

        self.person1.updated_data = {
            'name': 'person1',
            'weight': 50,
            'height': 160,
            'gender': 'female',
            'age': 30,
            'pal': '2.0'
        }
        self.person2.updated_data = {
            'name': 'person2',
            'weight': 80,
            'height': 180,
            'gender': 'male',
            'age': 30,
            'pal': '2.0'
        }

    def perform_request(self, user, token):
        self.client.force_login(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    # Tests for GET (list) requests
    def test_admin_read_person_list(self):
        self.perform_request(self.admin, self.admin_token)
        response = self.client.get('/api/persons/')
        self.assertEqual(response.status_code, 200)

    def test_owner_read_person_list(self):
        self.perform_request(self.owner, self.owner_token)
        response = self.client.get('/api/persons/')
        self.assertEqual(response.status_code, 403)

    def test_user_read_person_list(self):
        self.perform_request(self.user, self.user_token)
        response = self.client.get('/api/persons/')
        self.assertEqual(response.status_code, 403)

    def test_unauthorized_read_get_person_list(self):
        response = self.client.get('/api/persons/')
        self.assertEqual(response.status_code, 401)

    # Tests for GET (detail) requests
    def test_admin_read_person_detail(self):
        self.perform_request(self.admin, self.admin_token)
        response = self.client.get(f'/api/persons/{self.person1.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_owner_read_person_detail(self):
        self.perform_request(self.owner, self.owner_token)
        response_for_person1 = self.client.get(f'/api/persons/{self.person1.pk}/')
        response_for_person2 = self.client.get(f'/api/persons/{self.person2.pk}/')
        self.assertEqual(response_for_person1.status_code, 403)
        self.assertEqual(response_for_person2.status_code, 200)

    def test_user_read_person_detail(self):
        self.perform_request(self.user, self.user_token)
        response = self.client.get(f'/api/persons/{self.person1.pk}/')
        self.assertEqual(response.status_code, 403)

    def test_unauthorized_read_person_detail(self):
        response = self.client.get(f'/api/persons/{self.person1.pk}/')
        self.assertEqual(response.status_code, 401)

    # Tests for POST requests
    def test_admin_create_person(self):
        self.perform_request(self.admin, self.admin_token)
        response = self.client.post('/api/persons/', data={'name': 'person3'})
        self.assertEqual(response.status_code, 201)

    def test_owner_create_person(self):
        self.perform_request(self.owner, self.owner_token)
        response = self.client.post('/api/persons/', data={'name': 'person3'})
        self.assertEqual(response.status_code, 403)

    def test_user_create_person(self):
        self.perform_request(self.user, self.user_token)
        response = self.client.post('/api/persons/', data={'name': 'person3'})
        self.assertEqual(response.status_code, 403)

    def test_unauthorized_user_create_person(self):
        response = self.client.post('/api/persons/', data={'name': 'person3'})
        self.assertEqual(response.status_code, 401)

    # Tests for PUT requests
    def test_admin_update_person(self):
        self.perform_request(self.admin, self.admin_token)
        response = self.client.put(
            f'/api/persons/{self.person1.pk}/', data=self.person1.updated_data)
        self.assertEqual(response.status_code, 200)

    def test_owner_update_person(self):
        self.perform_request(self.owner, self.owner_token)
        response_for_person1 = self.client.put(
            f'/api/persons/{self.person1.pk}/', data=self.person1.updated_data)
        response_for_person2 = self.client.put(
            f'/api/persons/{self.person2.pk}/', data=self.person2.updated_data)
        self.assertEqual(response_for_person1.status_code, 403)
        self.assertEqual(response_for_person2.status_code, 200)

    def test_user_update_person(self):
        self.perform_request(self.user, self.user_token)
        response = self.client.put(
            f'/api/persons/{self.person1.pk}/', data=self.person1.updated_data)
        self.assertEqual(response.status_code, 403)

    def test_unauthorized_user_update_person(self):
        response = self.client.put(
            f'/api/persons/{self.person1.pk}/', data=self.person1.updated_data)
        self.assertEqual(response.status_code, 401)

    # Test for DELETE requests
    def test_admin_delete_person(self):
        self.perform_request(self.admin, self.admin_token)
        response = self.client.delete(f'/api/persons/{self.person1.pk}/')
        self.assertEqual(response.status_code, 204)

    def test_owner_delete_person(self):
        self.perform_request(self.owner, self.owner_token)
        response_for_person1 = self.client.delete(f'/api/persons/{self.person1.pk}/')
        response_for_person2 = self.client.delete(f'/api/persons/{self.person2.pk}/')
        self.assertEqual(response_for_person1.status_code, 403)
        self.assertEqual(response_for_person2.status_code, 403)

    def test_user_delete_person(self):
        self.perform_request(self.user, self.user_token)
        response = self.client.delete(f'/api/persons/{self.person1.pk}/')
        self.assertEqual(response.status_code, 403)

    def test_unauthorized_user_delete_person(self):
        response = self.client.delete(f'/api/persons/{self.person1.pk}/')
        self.assertEqual(response.status_code, 401)
