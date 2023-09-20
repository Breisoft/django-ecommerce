from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

import json

from .factories import UserFactory, ShoppingCartFactory, ShoppingCartItemFactory, ProductFactory

class ShoppingCartPermissionsTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Creating an authenticated user's cart
        self.user = UserFactory()
        self.user_cart = ShoppingCartFactory(user=self.user)
        self.refresh = RefreshToken.for_user(self.user) # Assuming you're using JWT tokens
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')

        # Creating an unauthenticated user's cart
        self.anon_cart = ShoppingCartFactory(user=None)
        
        # Creating another authenticated user's cart for conflict testing
        self.other_user = UserFactory()
        self.other_user_cart = ShoppingCartFactory(user=self.other_user)

        # Sample Product for adding to cart
        self.product = ProductFactory()

    # Test to ensure both authenticated and unauthenticated users can create carts
    def test_authenticated_create_cart(self):

        local_client = APIClient()

        local_user = UserFactory()
        refresh = RefreshToken.for_user(local_user)
        local_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        response = local_client.post('/api/cart/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_unauthenticated_create_cart(self):

        local_client = APIClient()
        response = local_client.post('/api/cart/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_no_list_all_carts(self):
        response = self.client.get(f'/api/cart/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    # Test to ensure users can list their own carts
    def test_list_own_cart(self):
        response = self.client.get(f'/api/cart/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    # Test to ensure users can't list other users' carts
    def test_list_other_cart(self):
        response = self.client.get(f'/api/cart/{self.other_user_cart.id}/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    # Test to ensure unauthenticated users can list their own carts (using the specific cart id)
    def test_list_anon_cart(self):

        local_client = APIClient()

        response = local_client.get(f'/api/cart/{self.anon_cart.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test to add products to cart
    def test_add_to_cart(self):
        data = {
            'product_id': self.product.id,
            'quantity': 3
        }
       
        response = self.client.post(
            f'/api/cart/{self.user_cart.id}/items/', 
            data=json.dumps(data), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data['product'], self.product.id)
        self.assertEqual(response.data['quantity'], 3)

    # Test to delete a product from the cart
    def test_delete_from_cart(self):
        item = ShoppingCartItemFactory(cart=self.user_cart, product=self.product)
        response = self.client.delete(f'/api/cart/{self.user_cart.id}/items/{item.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Test to clear an authenticated user's cart (delete all items)
    def test_clear_cart(self):
        response = self.client.delete(f'/api/cart/{self.user_cart.id}/items/clear/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Test to clear an unauthenticated user's cart (delete cart and all items)
    def test_clear_anon_cart(self):
        self.client.credentials()  # Removing credentials
        response = self.client.delete(f'/api/cart/{self.anon_cart.id}/items/clear/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.delete(f'/api/cart/{self.anon_cart.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # We never delete the cart for authenticated users, so no test for that scenario