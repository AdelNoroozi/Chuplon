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
