from rest_framework import serializers
from .models import *


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'customer', 'total_price','discount', 'address', 'status', 'post_tracking_code',)

    def create(self, validated_data):
        print(validated_data)
        print(self.data)
        validated_data["total_price"] = "0"
        print(validated_data)
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return


# def validate(self, attrs):

class CreateOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return
