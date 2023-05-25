import re

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, first_name=None, last_name=None, email=None, phone_number=None):
        if not username:
            raise ValueError('username is required')
        if not password:
            raise ValueError('password is required')
        user_obj = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number
        )
        user_obj.password = make_password(password)
        user_obj.is_staff = False
        user_obj.is_superuser = False
        user_obj.is_active = True
        user_obj.save(using=self._db)
        return user_obj

    def create_customer(self, username, password):
        email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
        if not email_pattern.match(username):
            raise ValueError('customer username must be an email')
        customer = self.create_user(
            username=username,
            password=password
        )
        customer.role = 'CUS'
        customer.email = username
        customer.save(using=self._db)
        Customer.objects.create(base_user=customer)
        return customer

    def create_print_provider(self, username, password, email, phone_number, first_name=None, last_name=None):
        print_provider = self.create_user(
            username=username,
            password=password,
            email=email,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
        )
        print_provider.role = 'PRP'
        print_provider.save(using=self._db)
        PrintProvider.objects.create(base_user=print_provider)
        return print_provider

    def create_admin(self, username, password, email, phone_number, first_name, last_name):
        admin = self.create_user(
            username=username,
            password=password,
            email=email,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
        )
        admin.is_staff = True
        admin.role = 'STF'
        admin.save(using=self._db)
        admin_object = Admin.objects.create(base_user=admin)
        admin_object.section = 'UD'
        admin_object.save(using=self._db)
        return admin

    def create_superuser(self, username, password):
        superuser = self.create_user(
            username=username,
            password=password
        )
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.role = 'SPU'
        superuser.save(using=self._db)
        return superuser


class BaseUser(AbstractUser):
    phone_number_validator = RegexValidator(regex=r'^(09)\d{9}$')

    ROLES = (('SPU', _('superuser')),
             ('STF', _('staff')),
             ('CUS', _('customer')),
             ('DES', _('designer')),
             ('PRP', _('print provider')))

    first_name = models.CharField(max_length=150, blank=True, null=True, verbose_name=_("first name"))
    last_name = models.CharField(max_length=150, blank=True, null=True, verbose_name=_("last name"), )
    email = models.EmailField(blank=True, null=True, verbose_name=_("email address"))
    modified_at = models.DateTimeField(auto_now=True, verbose_name=_('modified at'))
    phone_number = models.CharField(blank=True, null=True, validators=[phone_number_validator], max_length=30)
    role = models.CharField(choices=ROLES, max_length=20, verbose_name=_('role'))

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        if self.is_superuser:
            self.role = 'SPU'
            self.save()
        elif self.is_staff:
            self.role = 'STF'
            self.save()
        return f'{self.username} - {self.role}'

    class Meta:
        verbose_name = _('Base User')
        verbose_name_plural = _('Base Users')


class Customer(models.Model):
    base_user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='customer',
                                     verbose_name=_('base user'))
    birth_date = models.DateField(blank=True, null=True, verbose_name=_('birth date'))

    def __str__(self):
        return self.base_user.username

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')


class AccountVerification(models.Model):
    PURPOSES = (('REG', _('registration')),
                ('RTV', _('retrieval')),
                ('VAL', _('validation')))

    verifying_field = models.CharField(max_length=50, verbose_name=_('verifying field'))
    code = models.CharField(max_length=10, verbose_name=_('code'))
    purpose = models.CharField(max_length=10, choices=PURPOSES, verbose_name=_('purpose'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))

    def __str__(self):
        return f'{self.verifying_field} - {self.purpose} - {self.created_at}'

    class Meta:
        verbose_name = _('Account Verification')
        verbose_name_plural = _('Account Verifications')


class Designer(models.Model):
    card_number_validator = RegexValidator(regex=r'd{16}$')

    customer_object = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='designer',
                                           verbose_name=_('customer object'))
    card_number = models.CharField(max_length=20, validators=[card_number_validator], verbose_name=_('card number'))
    is_premium = models.BooleanField(default=False, verbose_name=_('is premium'))
    balance = models.FloatField(default=0, verbose_name=_('balance'))
    promotion_date = models.DateTimeField(auto_now_add=True, verbose_name=_('promotion date'))

    def __str__(self):
        return self.customer_object.base_user.username

    class Meta:
        verbose_name = _('Designer')
        verbose_name_plural = _('Designers')


class Store(models.Model):
    designer = models.ForeignKey(Designer, on_delete=models.CASCADE, related_name='stores', verbose_name=_('designer'))
    store_name = models.CharField(max_length=100, default=_('my store'), verbose_name=_('store name'))
    store_avatar = models.ImageField(
        blank=True,
        null=True,
        verbose_name='store avatar',
        upload_to='images/',
        default='images/default.png'
    )
    alt_text = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='avatar alternative text',
    )
    custom_url = models.CharField(max_length=100, verbose_name=_('custom url'))

    def __str__(self):
        return f'{self.store_name} - {self.designer.customer_object.base_user.username}'

    class Meta:
        verbose_name = _('Store')
        verbose_name_plural = _('Stores')


class Admin(models.Model):
    SECTIONS = (('UD', 'undefined'),)

    base_user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='admin',
                                     verbose_name=_('base user'))
    section = models.CharField(max_length=10, choices=SECTIONS, default='UD', verbose_name=_('section'))

    def __str__(self):
        return f'{self.base_user.first_name} {self.base_user.last_name} - {self.section}'

    class Meta:
        verbose_name = _('Admin')
        verbose_name_plural = _('Admins')


class PrintProvider(models.Model):
    base_user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='print_provider',
                                     verbose_name=_('base user'))
    name = models.CharField(max_length=50, default='unknown provider', verbose_name=_('name'))
    description = models.TextField(blank=True, null=True, verbose_name=_('description'))
    rate = models.IntegerField(default=0, blank=True, null=True, verbose_name=_('rate'))
    # state
    # city
    address_detail = models.TextField(max_length=500, blank=True, null=True, verbose_name=_('address detail'))
    post_code = models.BigIntegerField(blank=True, null=True, verbose_name=_('post code'))
    office_number = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('office number'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Print Provider')
        verbose_name_plural = _('Print Providers')

# Address
