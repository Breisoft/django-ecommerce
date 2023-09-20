from common.test_abstractions import ReadOnlyTestCaseMixin

from rest_framework.test import APITestCase

from .factories import CategoryFactory

class CategoryViewSetTestCase(ReadOnlyTestCaseMixin, APITestCase):
     
   factory = CategoryFactory
   list_url_name = 'category-list'
   detail_url_name = 'category-detail'
