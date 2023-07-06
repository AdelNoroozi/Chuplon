from django_filters.rest_framework import FilterSet

from design.models import BlankProduct


class BlankProductFilter(FilterSet):
    class Meta:
        model = BlankProduct
        fields = {
            'props': ['exact'],
            'category': ['exact']
        }
