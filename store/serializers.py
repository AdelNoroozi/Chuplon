from rest_framework import serializers

from design.models import BlankProductProviderPropDetail
from design.serializers import BlankProductFilterablePropValueSerializer
from store.models import Product
from utils.serializers import ColorSerializer


class ProductSerializer(serializers.ModelSerializer):
    designer = serializers.CharField(source="designer.customer_object.base_user.username")
    provider = serializers.CharField(source="provider.name")
    colors = ColorSerializer(many=True)
    props = serializers.SerializerMethodField()
    sizes = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_props(self, obj: Product):
        return BlankProductFilterablePropValueSerializer(obj.blank_product.props, many=True).data

    def get_sizes(self, obj: Product):
        sizes = []
        blank_product_provider_details = BlankProductProviderPropDetail.objects.filter(
            blankProductProviderProp__blank_product=obj.blank_product)
        for blank_product_provider_detail in blank_product_provider_details:
            sizes.append(blank_product_provider_detail.size.text)
        sizes = list(dict.fromkeys(sizes))
        return sizes


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ("discount_percent", "status", "rate", "store")


class ProductMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "prototype_image", "price", "discount_percent", "rate")
