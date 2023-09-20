from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from .models import Category
from .serializers import CategorySerializer

class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer