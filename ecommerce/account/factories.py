# factories.py
import factory
from django.contrib.auth.models import User
from .models import Address, Account

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda a: f"{a.username}@example.com")
    first_name = "John"
    last_name = "Doe"

class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    street = "123 Main St"
    city = "Anytown"
    state = "CA"
    zip_code = "90210"

class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Account

    user = factory.SubFactory(UserFactory)
    address = factory.SubFactory(AddressFactory)
