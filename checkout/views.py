from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import *
from .serializers import *

from rest_framework.generics import ListAPIView, RetrieveAPIView


class CreateOrderView(APIView):
    # def get(self, request):
    #     print("mame***************************************************")
    #     orders = Order.objects.all()
    #     serializer = CreateOrderSerializer(orders, many=True)
    #     return Response(serializer.data)

    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        if serializer.is_valid():
            # print(request.user()["id"]) ????
            order=serializer.save()

            sum_prices = 0
            for i in request.data["items"]:
                sum_prices += int(i["quantity"]) * Product.objects.get(id=i["product_id"]).price
                print(Order.objects.all().first())
                print(order)
                OrderItem.objects.create(
                    order=order,
                    product=Product.objects.get(id=i["product_id"]),
                    color=Color.objects.get(id=i["color_id"]),
                    quantity=i["quantity"]
                )
                # new_product_item.save()
                # print(serializer_item.validated_data.data)
            print(sum_prices)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
