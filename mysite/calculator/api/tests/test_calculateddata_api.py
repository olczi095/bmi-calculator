from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from calculator.models import Person

User = get_user_model()


class CalculateDataAPITest(APITestCase):
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
            name='person1',
        )
        self.person2 = Person.objects.create(
            user=self.owner,
            name='person2'
        )

    def perform_request(self, user, token):
        self.client.force_login(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    # Test for GET (list) requests
    def test_admin_read_calculateddata_list(self):
        self.perform_request(self.admin, self.admin_token)
        response = self.client.get(reverse('calculateddata-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_owner_read_calculateddata_list(self):
        self.perform_request(self.owner, self.owner_token)
        response = self.client.get(reverse('calculateddata-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_user_read_calculateddata_list(self):
        response = self.client.get(reverse('calculateddata-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Test for GET (detail) requests
    def test_admin_read_calculateddata_detail(self):
        self.perform_request(self.admin, self.admin_token)
        response = self.client.get(
            reverse('calculateddata-detail', args=[self.person1.calculated_data.pk])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_owner_read_calculatedddata_detail(self):
        self.perform_request(self.owner, self.owner_token)
        response_for_person1 = self.client.get(
            reverse('calculateddata-detail', args=[self.person1.calculated_data.pk])
        )
        response_for_person2 = self.client.get(
            reverse('calculateddata-detail', args=[self.person2.calculated_data.pk])
        )
        self.assertEqual(response_for_person1.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_for_person2.status_code, status.HTTP_200_OK)

    def test_user_read_calculateddata_detail(self):
        self.perform_request(self.user, self.user_token)
        response = self.client.get(
            reverse('calculateddata-detail', args=[self.person1.calculated_data.pk])
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_user_read_calculateddata_detail(self):
        response = self.client.get(
            reverse('calculateddata-detail', args=[self.person1.calculated_data.pk])
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Test for DELETE requests
    def test_admin_delete_calculateddata(self):
        self.perform_request(self.admin, self.admin_token)
        response = self.client.delete(
            reverse('calculateddata-detail', args=[self.person1.calculated_data.pk])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_owner_delete_calculatedddata(self):
        self.perform_request(self.owner, self.owner_token)
        response_for_person1 = self.client.delete(
            reverse('calculateddata-detail', args=[self.person1.calculated_data.pk])
        )
        response_for_person2 = self.client.delete(
            reverse('calculateddata-detail', args=[self.person2.calculated_data.pk])
        )
        self.assertEqual(response_for_person1.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_for_person2.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_delete_calculateddata(self):
        self.perform_request(self.user, self.user_token)
        response = self.client.delete(
            reverse('calculateddata-detail', args=[self.person1.calculated_data.pk])
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_delete_read_calculateddata(self):
        response = self.client.get(
            reverse('calculateddata-detail', args=[self.person1.calculated_data.pk])
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Test for POST requests, method not allowed to anyone
    def test_admin_create_calculateddata(self):
        self.perform_request(self.admin, self.admin_token)
        response = self.client.post(
            reverse('calculateddata-list'), data={'person3': self.person1}
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # Test for PUT requests, method not allowed to anyone
    def test_admin_update_calculateddata(self):
        self.perform_request(self.admin, self.admin_token)
        response = self.client.put(
            reverse('calculateddata-detail', args=[self.person1.calculated_data.pk]),
            data={'pal': 2.0}
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
