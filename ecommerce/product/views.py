from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer