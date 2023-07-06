from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination

from .filters import BlankProductFilter
from .models import Category, BlankProduct
from .serializers import CategorySerializer, BlankProductSerializer, BlankProductRetrieveSerializer, \
    CategoryRetrieveSerializer


class ListCategoryAPI(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class RetrieveCategoryAPI(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryRetrieveSerializer


class ListBLankProductAPI(ListAPIView):
    queryset = BlankProduct.objects.all()
    serializer_class = BlankProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BlankProductFilter
    pagination_class = PageNumberPagination


class RetrieveBLankProductAPI(RetrieveAPIView):
    queryset = BlankProduct.objects.all()
    serializer_class = BlankProductRetrieveSerializer
