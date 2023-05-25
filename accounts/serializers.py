import re

from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from rest_framework import serializers

from accounts.models import BaseUser, Customer, Admin


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        exclude = ('password',)


class AbstractUserTypeSerializer(serializers.ModelSerializer):
    base_user = BaseUserSerializer(many=False)

    class Meta:
        fields = '__all__'


class BaseUserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ('id', 'username', 'role')


class AbstractUserTypeMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'base_user')


# customer serializers
class RegisterCustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = BaseUser
        fields = ('username', 'password')

    def validate(self, attrs):
        email_validator = EmailValidator()
        username = attrs.get('username')
        if username:
            email_validator(username)
        # verifying email should be added later
        password = attrs.get('password')
        if password:
            validate_password(password)
        return attrs

    def create(self, validated_data):
        customer_user = self.Meta.model.objects.create_customer(**self.validated_data)
        return customer_user


class CustomerSerializer(AbstractUserTypeSerializer):
    class Meta(AbstractUserTypeSerializer.Meta):
        model = Customer


class CustomerMiniSerializer(AbstractUserTypeMiniSerializer):
    base_user = serializers.CharField(source='base_user.username')

    class Meta(AbstractUserTypeMiniSerializer.Meta):
        model = Customer


# admin serializers
class AddAdminSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = BaseUser
        fields = ('username', 'password', 'email', 'phone_number', 'first_name', 'last_name')

    def validate(self, attrs):
        email_validator = EmailValidator()
        email = attrs.get('email')
        if email:
            email_validator(email)
        phone_number_pattern = re.compile(r'^(09)\d{9}$')
        phone_number = attrs.get('phone_number')
        if phone_number:
            if not phone_number_pattern.match(phone_number):
                raise serializers.ValidationError('invalid phone number')
        password = attrs.get('password')
        if password:
            validate_password(password)
        return attrs

    def create(self, validated_data):
        admin_user = self.Meta.model.objects.create_admin(**self.validated_data)
        return admin_user


class AdminSerializer(AbstractUserTypeSerializer):
    class Meta(AbstractUserTypeSerializer.Meta):
        model = Admin


class AdminMiniSerializer(AbstractUserTypeMiniSerializer):
    base_user = serializers.SerializerMethodField(method_name='get_admin_name')

    class Meta(AbstractUserTypeMiniSerializer.Meta):
        model = Admin

    def get_admin_name(self, admin: Admin):
        return f'{admin.base_user.first_name} {admin.base_user.last_name}'

# admin serializers
# class AddProviderSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(required=True)
#     first_name = serializers.CharField(required=True)
#     last_name = serializers.CharField(required=True)
#     phone_number = serializers.CharField(required=True)
#     password = serializers.CharField(write_only=True, required=True)
#
#     class Meta:
#         model = BaseUser
#         fields = ('username', 'password', 'email', 'phone_number', 'first_name', 'last_name')
#
#     def validate(self, attrs):
#         email_validator = EmailValidator()
#         email = attrs.get('email')
#         if email:
#             email_validator(email)
#         phone_number_pattern = re.compile(r'^(09)\d{9}$')
#         phone_number = attrs.get('phone_number')
#         if phone_number:
#             if not phone_number_pattern.match(phone_number):
#                 raise serializers.ValidationError('invalid phone number')
#         password = attrs.get('password')
#         if password:
#             validate_password(password)
#         return attrs
#
#     def create(self, validated_data):
#         admin_user = self.Meta.model.objects.create_admin(**self.validated_data)
#         return admin_user
#
#
# class AdminSerializer(AbstractUserTypeSerializer):
#     class Meta(AbstractUserTypeSerializer.Meta):
#         model = Admin
#         fields = '__all__'
#
#
# class AdminMiniSerializer(serializers.ModelSerializer):
#     base_user = serializers.CharField(source='base_user.username')
#
#     class Meta:
#         model = Customer
#         fields = ('id', 'base_user')
