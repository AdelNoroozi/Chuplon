from django.contrib import admin
from .models import *


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "code",
        "percentage",
        "specific_user",

    )
    search_fields = ("title",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "total_price",
        "discount",
        "address",
        "status",
        "post_tracking_code",

    )
    search_fields = ("customer", "status", "post_tracking_code",)


