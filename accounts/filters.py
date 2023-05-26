from django_filters.rest_framework import FilterSet

from accounts.models import BaseUser, Admin, Designer, PrintProvider, Address, Store


class BaseUserFilter(FilterSet):
    class Meta:
        model = BaseUser
        fields = {
            'role': ['exact'],
            'is_active': ['exact'],
            'date_joined': ['gt', 'lt']

        }


class AdminFilter(FilterSet):
    class Meta:
        model = Admin
        fields = {
            'section': ['exact'],
        }


class DesignerFilter(FilterSet):
    class Meta:
        model = Designer
        fields = {
            'is_premium': ['exact'],
            'promotion_date': ['gt', 'lt'],
            'balance': ['gt', 'lt']
        }


class ProviderFilter(FilterSet):
    class Meta:
        model = PrintProvider
        fields = {
            'city': ['exact'],
            'city__state': ['exact']
        }


class AddressFilter(FilterSet):
    class Meta:
        model = Address
        fields = {
            'customer': ['exact'],
            'city': ['exact'],
            'city__state': ['exact']
        }


class StoreFilter(FilterSet):
    class Meta:
        model = Store
        fields = {
            'designer': ['exact'],
        }
