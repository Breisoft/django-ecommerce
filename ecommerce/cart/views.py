from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import ShoppingCart, ShoppingCartItem
from .serializers import ShoppingCartSerializer, ShoppingCartItemSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from common.base import UserOwnedModelViewSet


from product.models import Product

class CartItemViewSet(UserOwnedModelViewSet):
    serializer_class = ShoppingCartItemSerializer
    queryset = ShoppingCartItem.objects.all()
    lookup_field = 'id'
    user_field = 'cart__user'

    def create(self, request, id, *args, **kwargs):

        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        if not product_id or not quantity:
            return Response({'error': 'product_id and quantity are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the product exists.
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Invalid product_id'}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the cart belongs to the authenticated user.
        try:
            cart = ShoppingCart.objects.get(id=id, user=request.user)
        except ShoppingCart.DoesNotExist:
            return Response({'error': 'Cart not found or not owned by user'}, status=status.HTTP_404_NOT_FOUND)

        # Finding existing shopping cart item with associated product.
        shopping_cart_item, created = ShoppingCartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': quantity})

        if not created:
            shopping_cart_item.quantity += quantity
            shopping_cart_item.save()

        status_code = status.HTTP_204_NO_CONTENT if not created else status.HTTP_201_CREATED

        serializer = self.get_serializer(shopping_cart_item)
        return Response(serializer.data, status=status_code)
    
    # This is the custom action for deleting all items from the cart.
    @action(detail=True, methods=['delete'])
    def clear(self, request, id=None):
        # Ensure the cart belongs to the authenticated user.
        try:
            cart = ShoppingCart.objects.get(id=id, user=request.user)
        except ShoppingCart.DoesNotExist:
            return Response({'error': 'Cart not found or not owned by user'}, status=status.HTTP_404_NOT_FOUND)
        
        # Delete all items in the cart.
        cart.shoppingcartitem_set.all().delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class CartViewSet(UserOwnedModelViewSet):
    serializer_class = ShoppingCartSerializer
    queryset = ShoppingCart.objects.all()
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        # If user is authenticated, try to get their existing cart.
        if request.user.is_authenticated:
            shopping_cart, created = ShoppingCart.objects.get_or_create(user=request.user)
            status_code = status.HTTP_200_OK if not created else status.HTTP_201_CREATED
        else:  # If user is not authenticated, create a new anonymous cart.
            shopping_cart = ShoppingCart.objects.create(user=None)
            status_code = status.HTTP_201_CREATED

        serializer = self.get_serializer(shopping_cart)
        return Response(serializer.data, status=status_code)

