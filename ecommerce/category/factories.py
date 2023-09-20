from factory.django import DjangoModelFactory
from factory import Faker

from .models import Category

class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    slug = Faker('slug')
    name = Faker('name')