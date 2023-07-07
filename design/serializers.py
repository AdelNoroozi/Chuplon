from rest_framework import serializers
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
        fields = ("id", "title", "desc", "props", "category", "average_price")

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
    prop = BlankProductUnfilterablePropSerializer()

    class Meta:
        model = BlankProductUnfilterablePropValue
        fields = ("id", "prop", "value")


class BlankProductFilterablePropSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlankProductFilterableProp
        fields = ("id", "name")


class BlankProductFilterablePropValueSerializer(serializers.ModelSerializer):
    prop = BlankProductFilterablePropSerializer()

    class Meta:
        model = BlankProductFilterablePropValue
        fields = ("id", "prop", "value")


class BlankProductProviderPropSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlankProductProviderProp
        fields = ("id", "provider", "price", "prep_time")


class BlankProductProviderPropDetailSerializer(serializers.ModelSerializer):
    blankProductProviderProp = BlankProductProviderPropSerializer()

    class Meta:
        model = BlankProductProviderPropDetail
        fields = ("blankProductProviderProp", "color", "size", "price")


class BlankProductRetrieveSerializer(serializers.ModelSerializer):
    non_filterable_props = serializers.SerializerMethodField()
    filterable_props = serializers.SerializerMethodField()
    provider_prop_details = serializers.SerializerMethodField()

    class Meta:
        model = BlankProduct
        fields = (
            "id",
            "title",
            "desc",
            "props",
            "category",
            "non_filterable_props",
            "filterable_props",
            "provider_prop_details",
        )

    def get_non_filterable_props(self, obj):
        props = BlankProductUnfilterablePropValue.objects.filter(
            blank_product_id=obj.id
        )
        return BlankProductUnfilterablePropValueSerializer(props, many=True).data

    def get_filterable_props(self, obj):
        props = obj.props.all()
        return BlankProductFilterablePropValueSerializer(props, many=True).data

    def get_provider_prop_details(self, obj):
        provider_prop = BlankProductProviderProp.objects.filter(
            blank_product_id=obj.id
        ).first()
        provider_prop_detail = BlankProductProviderPropDetail.objects.filter(
            blankProductProviderProp_id=provider_prop.id
        )

        return BlankProductProviderPropDetailSerializer(
            provider_prop_detail, many=True
        ).data


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "parent",
            "is_active",
        )


