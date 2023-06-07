from django.db import models
from django.utils.translation import gettext_lazy as _


# class BaseModel(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
#     modified_at = models.DateTimeField(auto_now=True, verbose_name=_('modified at'))
#     created_by = models.ForeignKey(BaseUser, on_delete=models.RESTRICT, related_name='models_created_by_user')
#     modified_by = models.ForeignKey(BaseUser, on_delete=models.RESTRICT, related_name='models_modified_by_user')
#     is_active = models.BooleanField(default=True)


class State(models.Model):
    name = models.CharField(max_length=20, verbose_name=_('name'))

    class Meta:
        verbose_name = 'State'
        verbose_name_plural = 'States'

    def __str__(self):
        return self.name


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.RESTRICT, related_name='cities', verbose_name=_('state'))
    name = models.CharField(max_length=20, verbose_name=_('name'))

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name


class Size(models.Model):
    text = models.CharField(max_length=20, verbose_name=_('text'))

    class Meta:
        verbose_name = 'Size'
        verbose_name_plural = 'Sizes'

    def __str__(self):
        return self.text


class Color(models.Model):
    name = models.CharField(max_length=20, verbose_name=_('name'))
    code = models.CharField(max_length=20, verbose_name=_('code'))

    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colors'

    def __str__(self):
        return f' {self.name} - {self.code} '
