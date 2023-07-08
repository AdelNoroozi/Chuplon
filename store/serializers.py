from rest_framework import serializers

from store.models import Product
from utils.serializers import ColorSerializer


class ProductSerializer(serializers.ModelSerializer):
    colors = ColorSerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ("discount_percent", "status", "rate", "store")


class ProductMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("name", "prototype_image", "price", "discount_percent", "rate")
