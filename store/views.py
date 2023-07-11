from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from store.filters import ProductFilter
from store.models import Product
from store.serializers import ProductMiniSerializer, ProductSerializer, CreateProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(status="CON")
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['price']
    search_fields = ['name', 'desc']
    filterset_class = ProductFilter

    def get_serializer_class(self):
        if self.action == "list":
            return ProductMiniSerializer
        elif self.action == "create":
            return CreateProductSerializer
        else:
            return ProductSerializer
