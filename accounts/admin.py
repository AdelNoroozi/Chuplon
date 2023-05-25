from django.contrib import admin

from accounts.models import BaseUser, Customer

admin.site.register(BaseUser)
admin.site.register(Customer)
