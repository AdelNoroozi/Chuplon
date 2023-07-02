from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _
from utils.models import *
from accounts.models import PrintProvider


class Category(MPTTModel):
    name = models.CharField(max_length=20, unique=True, verbose_name=_('name'))
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name=_('parent'))
    is_active = models.BooleanField(default=False, verbose_name=_('is active'))

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return f'{self.name} - {self.parent}'


class BlankProductFilterableProp(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blank_product_filterable_props', verbose_name=_('category'))
    name = models.CharField(max_length=50, verbose_name=_('name'))

    class Meta:
        verbose_name = 'Blank Product Filterable Prop'
        verbose_name_plural = 'Blank Product Filterable Props'

    def __str__(self):
        return f'{self.category} - {self.name}'


class BlankProductFilterablePropValue(models.Model):
    prop = models.ForeignKey(BlankProductFilterableProp, on_delete=models.CASCADE, related_name='blank_product_filterable_prop_values', verbose_name=_('prop'))
    value = models.CharField(max_length=10, verbose_name=_('value'))

    class Meta:
        verbose_name = 'Blank Product Filterable Prop Value'
        verbose_name_plural = 'Blank Product Filterable Prop Values'

    def __str__(self):
        return f'{self.prop} : {self.value}'


class BlankProduct(models.Model):
    title = models.CharField(max_length=20, verbose_name=_('title'))
    desc = models.TextField(max_length=100, verbose_name=_('desc'))
    props = models.ManyToManyField(BlankProductFilterablePropValue, related_name='blank_products', verbose_name='props')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='blank_products', verbose_name='category')

    class Meta:
        verbose_name = 'Blank Product'
        verbose_name_plural = 'Blank Products'

    def __str__(self):
        return f'{self.title} - {self.category}'


class BlankProductUnfilterableProp(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blank_product_unfilterable_props', verbose_name='category')
    name = models.CharField(max_length=50, verbose_name=_('name'))

    class Meta:
        verbose_name = 'Blank Product Unfilterable Prop'
        verbose_name_plural = 'Blank Product Unfilterable Props'

    def __str__(self):
        return f'{self.category} - {self.name}'


class BlankProductUnfilterablePropValue(models.Model):
    blank_product = models.ForeignKey(BlankProduct, on_delete=models.CASCADE, related_name='blank_product_unfilterable_prop_values', verbose_name='blank product')
    prop = models.ForeignKey(BlankProductUnfilterableProp, on_delete=models.CASCADE, related_name='blank_product_unfilterable_prop_values', verbose_name='prop')
    value = models.CharField(max_length=10, verbose_name=_('value'))

    class Meta:
        verbose_name = 'Blank Product Unfilterable PropValue'
        verbose_name_plural = 'Blank Product Unfilterable PropValues'

    def __str__(self):
        return f'{self.blank_product} - {self.prop} : {self.value}'


class BlankProductImage(models.Model):
    blank_product = models.ForeignKey(BlankProduct, on_delete=models.CASCADE, related_name='blank_product_images', verbose_name=_('blank product'))
    image = models.ImageField(verbose_name=_('image'))
    alt_text = models.CharField(max_length=50, verbose_name=_('alt text'))
    is_preview = models.BooleanField(verbose_name=_('is preview'))

    class Meta:
        verbose_name = 'Blank Product Image'
        verbose_name_plural = 'Blank Product Images'

    def __str__(self):
        return self.blank_product


class BlankProductSampleImage(models.Model):
    blank_product = models.ForeignKey(BlankProduct, on_delete=models.CASCADE, related_name='blank_product_sample_images', verbose_name=_('blank product'))
    file = models.FileField(verbose_name=_('file'))

    class Meta:
        verbose_name = 'Blank Product Sample Image'
        verbose_name_plural = 'Blank Product Sample Images'

    def __str__(self):
        return self.blank_product


class BlankProductProviderProp(models.Model):
    blank_product = models.ForeignKey(BlankProduct, on_delete=models.CASCADE, related_name='blank_product_provider_props', verbose_name=_('blank product'))
    provider = models.ForeignKey(PrintProvider, on_delete=models.SET_NULL, null=True, related_name='blank_product_provider_props', verbose_name=_('provider'))
    price = models.CharField(max_length=10, verbose_name=_('price'))
    prep_time = models.CharField(max_length=10, verbose_name=_('prep time'))

    class Meta:
        verbose_name = 'Blank Product Provider Prop'
        verbose_name_plural = 'Blank Product Provider Props'

    def __str__(self):
        return f'{self.blank_product} by {self.provider} : {self.price}'


class BlankProductProviderPropDetail(models.Model):
    blankProductProviderProp = models.ForeignKey(BlankProductProviderProp, on_delete=models.CASCADE, related_name='blank_product_provider_prop_details', verbose_name=_('blank product provider prop'))
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, related_name='blank_product_provider_prop_details', verbose_name=_('color'))
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, related_name='blank_product_provider_prop_details', verbose_name=_('price'))
    price = models.CharField(max_length=10, verbose_name=_('price'))

    class Meta:
        verbose_name = 'Blank Product Provider Prop Detail'
        verbose_name_plural = 'Blank Product Provider Prop Details'

    def __str__(self):
        return self.blankProductProviderProp
