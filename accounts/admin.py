from django.contrib import admin

from accounts.models import BaseUser, Customer, Admin

admin.site.register(BaseUser)
admin.site.register(Customer)
admin.site.register(Admin)
