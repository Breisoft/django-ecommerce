from factory import Faker, SubFactory
from factory.django import DjangoModelFactory
from .models import Product

from category.factories import CategoryFactory

class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product
    
    slug = Faker('slug')
    name = Faker('name')
    description = Faker('sentence', nb_words=5)
    price = Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
    quantity = Faker('random_digit_not_null')
    is_active = Faker('boolean')
    created_at = Faker('past_datetime')
    updated_at = Faker('past_datetime')


    category = SubFactory(CategoryFactory)
