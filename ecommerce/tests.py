from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from account.models import Address
from django.test import TestCase

from account.factories import AccountFactory

class JWTAuthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.account = AccountFactory()

        self.refresh = RefreshToken.for_user(self.account.user)

        self.protected_endpoint = '/api/account/me/'

    def test_access_protected_view(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        response = self.client.get(self.protected_endpoint)
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_access_to_protected_view(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer badtoken')
        response = self.client.get(self.protected_endpoint)
        self.assertEqual(response.status_code, 401)

    def test_no_credentials_access_to_protected_view(self):
        response = self.client.get(self.protected_endpoint)
        self.assertEqual(response.status_code, 401)
