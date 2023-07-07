from django.db import models
from accounts.models import *
from django.utils.translation import gettext_lazy as _


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
        BaseUser,  # TODO
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name=_('customer')
    )

    class Meta:
        verbose_name = 'Discount'
        verbose_name_plural = 'Discounts'

    def __str__(self):
        return f'{self.title} - {self.percentage} for " {self.specific_user} " code : {self.code}'


class Order(models.Model):
    customer = models.ForeignKey(
        Customer,
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
        Customer,
        on_delete=models.RESTRICT,
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
        max_length=20,
        verbose_name=_('status')
    )
    post_tracking_code = models.CharField(  # TODO
        max_length=20,
        verbose_name=_('post_tracking_code')
    )

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'{self.customer} - {self.total_price}$ " status : {self.status}'
