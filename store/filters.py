from django_filters.rest_framework import FilterSet

from store.models import Product


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'blank_product__props': ['exact'],
            'blank_product__category': ['exact']
        }
