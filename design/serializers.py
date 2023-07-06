from rest_framework import serializers

from accounts.serializers import ProviderSerializer, ProviderMiniSerializer, ProviderBlankProductSerializer
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("id", "name", "parent", "children")

    def get_children(self, obj):
        children = Category.objects.filter(parent=obj)
        serializer = self.__class__(children, many=True)
        return serializer.data


class BlankProductSerializer(serializers.ModelSerializer):
    average_price = serializers.SerializerMethodField()

    class Meta:
        model = BlankProduct
        fields = ("id", "title", "category", "average_price")

    def get_average_price(self, obj):
        prices = BlankProductProviderProp.objects.filter(
            blank_product_id=obj.id
        ).values("price")
        average_price = 0
        for price in prices:
            average_price += int(price["price"])
        average_price /= len(prices)

        return average_price


class BlankProductUnfilterablePropSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlankProductUnfilterableProp
        fields = ("id", "name")


class BlankProductUnfilterablePropValueSerializer(serializers.ModelSerializer):
    prop = serializers.CharField(source="prop.name")

    class Meta:
        model = BlankProductUnfilterablePropValue
        fields = ("id", "prop", "value")


class BlankProductFilterablePropValueSerializer(serializers.ModelSerializer):
    prop = serializers.CharField(source="prop.name")

    class Meta:
        model = BlankProductFilterablePropValue
        fields = ("id", "prop", "value")


class FilterColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlankProductFilterableProp
        fields = ("id", "name")


class CategoryRetrieveSerializer(serializers.ModelSerializer):
    blank_product_filterable_props = FilterColumnSerializer(many=True)

    class Meta:
        model = Category
        fields = ("id", "name", "blank_product_filterable_props")


class BlankProductProviderPropSerializer(serializers.ModelSerializer):
    provider = ProviderBlankProductSerializer(many=False)

    class Meta:
        model = BlankProductProviderProp
        fields = ("id", "provider", "price", "prep_time")


class BlankProductProviderPropDetailSerializer(serializers.ModelSerializer):
    blankProductProviderProp = BlankProductProviderPropSerializer()

    class Meta:
        model = BlankProductProviderPropDetail
        fields = ("blankProductProviderProp", "color", "size", "price")


class BlankProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlankProductImage
        exclude = ("blank_product",)


class BlankProductRetrieveSerializer(serializers.ModelSerializer):
    blank_product_unfilterable_prop_values = BlankProductUnfilterablePropValueSerializer(many=True)
    props = BlankProductFilterablePropValueSerializer(many=True)
    blank_product_provider_props = BlankProductProviderPropSerializer(many=True)
    blank_product_images = BlankProductImageSerializer(many=True)

    class Meta:
        model = BlankProduct
        fields = (
            "id",
            "title",
            "desc",
            "category",
            "props",
            "blank_product_unfilterable_prop_values",
            "blank_product_provider_props",
            "blank_product_images",
        )
