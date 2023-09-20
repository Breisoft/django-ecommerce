from common.test_abstractions import ReadOnlyTestCaseMixin

from rest_framework.test import APITestCase

from .factories import ProductFactory

class ProductyViewSetTestCase(ReadOnlyTestCaseMixin, APITestCase):

    factory = ProductFactory
    list_url_name = 'product-list'
    detail_url_name = 'product-detail'