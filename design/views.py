from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination

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
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = []
    ordering_fields = []
    pagination_class = PageNumberPagination

    queryset = BlankProduct.objects.all()
    serializer_class = BlankProductRetrieveSerializer