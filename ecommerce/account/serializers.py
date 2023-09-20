from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Address, Account
from django.db import transaction


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street', 'city', 'state', 'zip_code']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    address = AddressSerializer()

    class Meta:
        model = Account
        fields = ['user', 'address']

    @transaction.atomic
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)

        address_data = validated_data.pop('address')
        address = Address.objects.create(**address_data)

        account = Account.objects.create(user=user, address=address, **validated_data)
        return account

    @transaction.atomic
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        # Set user UPDATE fields
        for attr, value in user_data.items():
            setattr(user, attr, value)

        address_data = validated_data.pop('address', {})
        address = instance.address

        # Set address UPDATE fields
        for attr, value in address_data.items():
            setattr(address, attr, value)

        # Set account UPDATE fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        user.save()
        address.save()
        instance.save()

        return instance


