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

