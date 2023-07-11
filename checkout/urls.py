from django.urls import path
from .views import *

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

urlpatterns = [
    path("order/", CreateOrderView.as_view(), name="order"),
]
