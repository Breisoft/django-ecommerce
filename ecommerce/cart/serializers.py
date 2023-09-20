from rest_framework import serializers
from .models import ShoppingCart, ShoppingCartItem

from product.models import Product
from product.serializers import ProductSerializer

class ShoppingCartItemSerializer(serializers.ModelSerializer):

    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = ShoppingCartItem
        fields = ['product', 'quantity']


class ShoppingCartSerializer(serializers.ModelSerializer):

    items = ShoppingCartItemSerializer(source='shoppingcartitem_set', many=True)


    class Meta:
        model = ShoppingCart
        fields = ['id', 'user', 'items']


