from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Account

from account.factories import AccountFactory

class AccountCreateTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_account_with_valid_data(self):
        url = reverse('account-list')  # Assuming you named your AccountViewSet URL 'account-list'
        data = {
            "user": {
                "username": "testuser",
                "email": "testuser@example.com",
                "first_name": "Test",
                "last_name": "User",
                "password": "password1234"
            },
            "address": {
                "street": "1234 Elm Street",
                "city": "Springfield",
                "state": "IL",
                "zip_code": "62704"
            }
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(get_user_model().objects.filter(email="testuser@example.com").exists())
        self.assertTrue(Account.objects.filter(user__email="testuser@example.com").exists())

    def test_create_account_with_invalid_data(self):

        url = reverse('account-list')
        data = {
            "user": {
                "username": "",
                "email": "testuser",
                "first_name": "",
                "last_name": "",
                "password": "password1234"
            },
            "address": {
                "street": "",
                "city": "",
                "state": "",
                "zip_code": ""
            }
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(get_user_model().objects.filter(email="testuser").exists())


class AccountPermissionsTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Account is authenticated
        self.account = AccountFactory()
        self.refresh = RefreshToken.for_user(self.account.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')

        # Account two is not authenticated
        self.account_two = AccountFactory()

    def test_no_list_all_accounts(self):
        response = self.client.get(f'/api/account/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Test to ensure the logged-in user can retrieve their own account details
    def test_list_me_account(self):
        response = self.client.get('/api/account/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test to ensure a user cannot retrieve details of someone else's account
    def test_list_other_account(self):
        response = self.client.get(f'/api/account/{self.account_two.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Test to ensure the logged-in user can update their own account details
    def test_update_own_account(self):
        update_data = {'user': {'username': 'updated_name'}}
        response = self.client.patch(f'/api/account/{self.account.user.id}/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], 'updated_name')

    # Test to ensure a user cannot update someone else's account
    def test_update_other_account(self):
        update_data = {'user': {'username': 'try_update'}}
        response = self.client.patch(f'/api/account/{self.account_two.user.id}/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Test to ensure the logged-in user can delete their own account
    def test_delete_own_account(self):
        response = self.client.delete(f'/api/account/{self.account.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Test to ensure a user cannot delete someone else's account
    def test_delete_other_account(self):
        response = self.client.delete(f'/api/account/{self.account_two.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)