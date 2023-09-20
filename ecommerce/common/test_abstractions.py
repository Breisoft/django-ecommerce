import unittest

# Create your tests here.
from django.urls import reverse
from rest_framework import status

class ReadOnlyTestCaseMixin:

    factory = None
    list_url_name = None
    detail_url_name = None

    def setUp(self):

        self.instance = self.factory.create()
        self.list_url = reverse(self.list_url_name)
        self.detail_url = reverse(self.detail_url_name, args=[self.instance.id])

    def test_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_retrieve(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.instance.id)

    def test_create_not_allowed(self):
        response = self.client.post(self.list_url, data={'name': 'New Item'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_not_allowed(self):
        response = self.client.put(self.detail_url, data={'name': 'Updated Name'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_not_allowed(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
