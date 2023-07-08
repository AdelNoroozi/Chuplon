from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import Designer, PrintProvider, Store
from design.models import BlankProduct
from utils.models import Color


class Product(models.Model):
    STATUSES = (("DES", _("designed")),
                ("CON", _("confirmed")),
                ("REJ", _("rejected")))
    name = models.CharField(max_length=50, verbose_name=_("name"))
    desc = models.TextField(verbose_name=_("desc"))
    blank_product = models.ForeignKey(BlankProduct, on_delete=models.RESTRICT, related_name="products",
                                      verbose_name=_("blank product"))
    designer = models.ForeignKey(Designer, on_delete=models.RESTRICT, related_name="designed_products",
                                 verbose_name=_("designer"))
    provider = models.ForeignKey(PrintProvider, on_delete=models.RESTRICT, related_name="products",
                                 verbose_name=_("provider"))
    design_image = models.ImageField(verbose_name=_("design_image"))
    prototype_image = models.ImageField(verbose_name=_("prototype image"))
    price = models.FloatField(verbose_name=_("price"))
    discount_percent = models.IntegerField(default=0, verbose_name=_("discount percent"))
    status = models.CharField(max_length=20, choices=STATUSES, default="DES", verbose_name=_("status"))
    rate = models.DecimalField(max_digits=2, decimal_places=1, default=0.0, verbose_name=_("rate"))
    colors = models.ManyToManyField(Color, related_name="products", verbose_name=_("colors"))
    store = models.ForeignKey(Store, on_delete=models.RESTRICT, related_name="products", blank=True, null=True,
                              verbose_name=_("store"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
