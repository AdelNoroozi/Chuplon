from django.contrib import admin
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "parent",
        "is_active",

    )
    search_fields = ("name",)
    list_filter = ("is_active",)

@admin.register(BlankProductFilterablePropValue)
class BlankProductFilterablePropValueAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "prop",
        "value",

    )
    search_fields = ("value","prop")


@admin.register(BlankProductFilterableProp)
class BlankProductFilterablePropAdmin(admin.ModelAdmin):
    # inlines = (BlankProductFilterablePropValueAdmin, )
    list_display = (
        "id",
        "category",
        "name",

    )
    search_fields = ("name",)


@admin.register(BlankProduct)
class BlankProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "desc",
        "category",

    )
    search_fields = ("title",)


@admin.register(BlankProductUnfilterableProp)
class BlankProductUnfilterablePropAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "category",
        "name",
    )
    search_fields = ("name",)


@admin.register(BlankProductUnfilterablePropValue)
class BlankProductUnfilterablePropValueAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "blank_product",
        "prop",
        "value",
    )
    search_fields = ("value",)


@admin.register(BlankProductImage)
class BlankProductImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "blank_product",
        "image",
        "alt_text",
        "is_preview",
    )
    search_fields = ("value",)
    list_filter = ("is_preview",)


@admin.register(BlankProductSampleImage)
class BlankProductSampleImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "blank_product",
        "file",
    )


@admin.register(BlankProductProviderProp)
class BlankProductProviderPropAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "blank_product",
        "provider",
        "price",
        "prep_time",
    )
    search_fields = ("provider",)


@admin.register(BlankProductProviderPropDetail)
class BlankProductProviderPropDetailAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "blankProductProviderProp",
        "color",
        "size",
        "price",
    )