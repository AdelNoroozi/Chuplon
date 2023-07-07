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
        BaseUser,
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


