from django.contrib import admin

from accounts.models import BaseUser, Customer, Admin, PrintProvider, Designer, Store, Address

admin.site.register(BaseUser)
admin.site.register(Customer)
admin.site.register(Admin)
admin.site.register(PrintProvider)
admin.site.register(Designer)
admin.site.register(Store)
admin.site.register(Address)
