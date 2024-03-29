import re

from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from accounts.models import BaseUser, Customer, Admin, PrintProvider, Designer, Store, Address


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
        fields = ('id', 'base_user')


class AbstractAddUserTypeSerializer(serializers.ModelSerializer):
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
class AddAdminSerializer(AbstractAddUserTypeSerializer):

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


# provider serializers
class AddProviderSerializer(AbstractAddUserTypeSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    def create(self, validated_data):
        provider_user = self.Meta.model.objects.create_print_provider(**self.validated_data)
        return provider_user


class ProviderSerializer(AbstractUserTypeSerializer):
    class Meta(AbstractUserTypeSerializer.Meta):
        model = PrintProvider


class ProviderMiniSerializer(AbstractUserTypeMiniSerializer):
    class Meta(AbstractUserTypeMiniSerializer.Meta):
        model = PrintProvider
        fields = ('id', 'base_user', 'name')


class ProviderBlankProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrintProvider
        fields = ("id", "name", "address_detail")


# designer serializers
class DesignerSerializer(AbstractUserTypeSerializer):
    base_user = None
    customer_object = CustomerSerializer(many=False)

    class Meta(AbstractUserTypeSerializer.Meta):
        model = Designer


class DesignerMiniSerializer(AbstractUserTypeMiniSerializer):
    customer_object = serializers.CharField(source='customer_object.base_user.username')

    class Meta(AbstractUserTypeMiniSerializer.Meta):
        model = Designer
        fields = ('id', 'customer_object')


# store serializers
class SaveStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        exclude = ('designer',)

    def save(self, **kwargs):
        designer_id = get_object_or_404(Designer, customer_object__base_user=self.context['request'].user).id
        store_name = self.validated_data.get('store_name')
        store_avatar = self.validated_data.get('store_avatar')
        custom_url = self.validated_data.get('custom_url')
        store_id = self.context['store_id']
        if store_id:
            store = get_object_or_404(Store, id=store_id)
            store.store_name = store_name or store.store_name
            store.store_avatar = store_avatar
            store.custom_url = custom_url
            store.save()
            self.instance = store
        else:
            if not Designer.objects.filter(id=designer_id).exists():
                raise serializers.ValidationError('designer not found')
            self.instance = Store.objects.create(designer_id=designer_id,
                                                 store_name=store_name or Store._meta.get_field('store_name').default,
                                                 store_avatar=store_avatar, custom_url=custom_url)

        return self.instance


class StoreSerializer(serializers.ModelSerializer):
    designer = DesignerMiniSerializer(many=False)

    class Meta:
        model = Store
        fields = '__all__'


# address serializers
class SaveAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ('customer',)

    def save(self, **kwargs):
        customer_id = get_object_or_404(Customer, base_user=self.context['request'].user).id
        city = self.validated_data.get('city')
        detail = self.validated_data.get('detail')
        post_code = self.validated_data.get('post_code')
        phone_number = self.validated_data.get('phone_number')
        is_default = self.validated_data.get('is_default')
        address_id = self.context['address_id']
        if address_id:
            address = get_object_or_404(Address, id=address_id)
            address.city = city
            address.detail = detail
            address.post_code = post_code
            address.phone_number = phone_number
            address.is_default = is_default
            address.save()
            self.instance = address
        else:
            if not Customer.objects.filter(id=customer_id).exists():
                raise serializers.ValidationError('customer not found')
            self.instance = Address.objects.create(customer_id=customer_id, city=city, detail=detail,
                                                   post_code=post_code, phone_number=phone_number,
                                                   is_default=is_default)

            return self.instance


class AddressSerializer(serializers.ModelSerializer):
    customer = CustomerMiniSerializer(many=False)

    class Meta:
        model = Address
        fields = '__all__'


class ChangePasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = BaseUser
        fields = ('current_password', 'new_password')

    def validate(self, attrs):
        current_password = attrs.get('current_password')
        new_password = attrs.get('new_password')
        if not current_password:
            raise serializers.ValidationError({'missing field': 'current password'})
        if not new_password:
            raise serializers.ValidationError({'missing field': 'new password'})
        user = self.context['request'].user
        if not user.check_password(current_password):
            raise serializers.ValidationError({'invalid fields': 'incorrect password.'})
        if current_password == new_password:
            raise serializers.ValidationError({'invalid field': 'old password and new password are the same.'})
        return attrs

    def update(self, instance, validated_data):
        instance.password = make_password(validated_data['new_password'])
        instance.save()
        return instance
