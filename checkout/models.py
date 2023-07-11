from django.db import models
from accounts.models import *
from django.utils.translation import gettext_lazy as _
from design.models import *
from utils.models import *
from store.models import *


class Discount(models.Model):
    title = models.CharField(
        max_length=20,
        verbose_name=_('title')
    )
    code = models.CharField(
        max_length=30,
        verbose_name=_('code')
    )
    percentage = models.CharField(
        max_length=5,
        verbose_name=_('percentage')
    )
    specific_user = models.ForeignKey(
        Customer,  # TODO
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='discounts',
        verbose_name=_('specific user')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at')
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('modified at')
    )

    class Meta:
        verbose_name = 'Discount'
        verbose_name_plural = 'Discounts'

    def __str__(self):
        return f'{self.title} - {self.percentage} for " {self.specific_user} " code : {self.code}'


class Order(models.Model):
    customer = models.ForeignKey(
        Customer,
        blank=True,  # TODO remove this,only for test
        null=True,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name=_('customer')
    )
    total_price = models.CharField(
        max_length=10,
        verbose_name=_('total_price')
    )
    discount = models.ForeignKey(
        Discount,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='orders',
        verbose_name=_('discount')
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.RESTRICT,
        blank=True,  # TODO remove this,only for test
        null=True,  # TODO remove this,only for test
        related_name='orders',
        verbose_name=_('address')
    )
    status_choice = (
        ('REQ', _('requested')),
        ('CNL', _('canceled')),
        ('CON', _('confirmed')),
        ('PRP', _('preparing')),
        ('SHP', _('shipping')),
        ('DEL', _('delivered')),
    )
    status = models.CharField(
        choices=status_choice,
        default='REQ',
        max_length=20,
        verbose_name=_('status')
    )
    post_tracking_code = models.CharField(  # TODO
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_('post_tracking_code')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at')
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('modified at')
    )

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'{self.customer} - {self.total_price}$ " status : {self.status}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name=_('order')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,  # TODO models.DO_NOTHING ?
        related_name='order_items',
        verbose_name=_('product')
    )
    color = models.ForeignKey(
        Color,
        on_delete=models.RESTRICT,
        related_name='order_items',
        verbose_name=_('color')
    )
    size = models.ForeignKey(
        Size,
        on_delete=models.RESTRICT,
        blank=True,
        null=True,
        related_name='order_items',
        verbose_name=_('size')
    )
    quantity = models.CharField(
        max_length=10,
        verbose_name=_('quantity')
    )

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f'{self.order} - {self.product}'


class Payment(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        blank=True,
        related_name='payments',
        verbose_name=_('order')
    )
    type_choice = (
        ('INC ', _('income')),
        ('RTN', _('return')),
        ('WDL', _('withdrawal')),
    )
    type = models.CharField(
        choices=type_choice,
        max_length=20,
        verbose_name=_('type')
    )
    receipt_file = models.CharField(  # TODO ??
        max_length=10,
        verbose_name=_('receipt_file')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at')
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('modified at')
    )

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return f'{self.order} - {self.type}'
