from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Category, BlankProduct
from .serializers import CategorySerializer, BlankProductSerializer, BlankProductRetrieveSerializer


class ListCategoryAPI(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class RetrieveCategoryAPI(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ListBLankProductAPI(ListAPIView):
    queryset = BlankProduct.objects.all()
    serializer_class = BlankProductSerializer


class RetrieveBLankProductAPI(RetrieveAPIView):
    queryset = BlankProduct.objects.all()
    serializer_class = BlankProductRetrieveSerializer