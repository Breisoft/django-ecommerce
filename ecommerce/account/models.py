from django.db import models

from django.contrib.auth import get_user_model

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)

class Account(models.Model):

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, primary_key=True)
    email_confirmed = models.BooleanField(default=False)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)



