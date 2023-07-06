from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent', 'children')

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
        prices = BlankProductProviderProp.objects.filter(blank_product_id=obj.id).values("price")
        average_price = 0
        for price in prices:
            average_price += int(price["price"])
        average_price /= len(prices)

        return average_price


class BlankProductUnfilterablePropSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlankProductFilterableProp
        fields = "__all__"


class BlankProductUnfilterablePropValueSerializer(serializers.ModelSerializer):
    prop = BlankProductUnfilterablePropSerializer()

    class Meta:
        model = BlankProductUnfilterablePropValue
        fields = ("id", "blank_product", "prop", "value")
