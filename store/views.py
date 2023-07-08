from rest_framework import viewsets

from store.models import Product
from store.serializers import ProductMiniSerializer, ProductSerializer, CreateProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(status="CON")

    def get_serializer_class(self):
        if self.action == "list":
            return ProductMiniSerializer
        elif self.action == "create":
            return CreateProductSerializer
        else:
            return ProductSerializer
