import factory
from django.contrib.auth.models import User
from product.models import Product
from product.factories import ProductFactory
from .models import ShoppingCart, ShoppingCartItem

from account.factories import UserFactory

class ShoppingCartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShoppingCart

    user = factory.SubFactory(UserFactory)

class ShoppingCartItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShoppingCartItem

    product = factory.SubFactory(ProductFactory)
    quantity = factory.Iterator([1, 2, 3, 4, 5])
    cart = factory.SubFactory(ShoppingCartFactory)
