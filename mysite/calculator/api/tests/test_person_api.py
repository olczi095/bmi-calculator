from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
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
        response = self.client.get(reverse('person-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_owner_read_person_list(self):
        self.perform_request(self.owner, self.owner_token)
        response = self.client.get(reverse('person-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_read_person_list(self):
        self.perform_request(self.user, self.user_token)
        response = self.client.get(reverse('person-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_read_get_person_list(self):
        response = self.client.get(reverse('person-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Tests for GET (detail) requests
    def test_admin_read_person_detail(self):
        self.perform_request(self.admin, self.admin_token)
        response = self.client.get(reverse('person-detail', args=[self.person1.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_owner_read_person_detail(self):
        self.perform_request(self.owner, self.owner_token)
        response_for_person1 = self.client.get(
            reverse('person-detail', args=[self.person1.pk]))
        response_for_person2 = self.client.get(
            reverse('person-detail', args=[self.person2.pk]))
        self.assertEqual(response_for_person1.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_for_person2.status_code, status.HTTP_200_OK)

    def test_user_read_person_detail(self):
        self.perform_request(self.user, self.user_token)
        response = self.client.get(reverse('person-detail', args=[self.person1.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_read_person_detail(self):
        response = self.client.get(reverse('person-detail', args=[self.person1.pk]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Tests for POST requests
    def test_admin_create_person(self):
        self.perform_request(self.admin, self.admin_token)
        response = self.client.post(reverse('person-list'), data={'name': 'person3'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_owner_create_person(self):
        self.perform_request(self.owner, self.owner_token)
        response = self.client.post(reverse('person-list'), data={'name': 'person3'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_create_person(self):
        self.perform_request(self.user, self.user_token)
        response = self.client.post(reverse('person-list'), data={'name': 'person3'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_user_create_person(self):
        response = self.client.post(reverse('person-list'), data={'name': 'person3'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Tests for PUT requests
    def test_admin_update_person(self):
        self.perform_request(self.admin, self.admin_token)
        data = self.person1.updated_data
        response = self.client.put(
            reverse('person-detail', args=[self.person1.pk]), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_owner_update_person(self):
        self.perform_request(self.owner, self.owner_token)
        person1_data = self.person1.updated_data
        person2_data = self.person2.updated_data
        response_for_person1 = self.client.put(
            reverse('person-detail', args=[self.person1.pk]), data=person1_data
        )
        response_for_person2 = self.client.put(
            reverse('person-detail', args=[self.person2.pk]), data=person2_data
        )
        self.assertEqual(response_for_person1.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_for_person2.status_code, status.HTTP_200_OK)

    def test_user_update_person(self):
        self.perform_request(self.user, self.user_token)
        data = self.person1.updated_data
        response = self.client.put(
            reverse('person-detail', args=[self.person1.pk]), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_user_update_person(self):
        data = self.person1.updated_data
        response = self.client.put(
            reverse('person-detail', args=[self.person1.pk]), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Test for DELETE requests
    def test_admin_delete_person(self):
        self.perform_request(self.admin, self.admin_token)
        response = self.client.delete(reverse('person-detail', args=[self.person1.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_owner_delete_person(self):
        self.perform_request(self.owner, self.owner_token)
        response_for_person1 = self.client.delete(
            reverse('person-detail', args=[self.person1.pk])
        )
        response_for_person2 = self.client.delete(
            reverse('person-detail', args=[self.person2.pk])
        )
        self.assertEqual(response_for_person1.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_for_person2.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_delete_person(self):
        self.perform_request(self.user, self.user_token)
        response = self.client.delete(reverse('person-detail', args=[self.person1.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_user_delete_person(self):
        response = self.client.delete(reverse('person-detail', args=[self.person1.pk]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
