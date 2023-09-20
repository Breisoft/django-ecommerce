from django.contrib.auth.models import User
from django.db import models
from product.models import Product


class ShoppingCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

class ShoppingCartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)

