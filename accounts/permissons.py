from rest_framework.permissions import DjangoModelPermissions, BasePermission, SAFE_METHODS

from accounts.models import Store, Designer, Address, Customer


class MappedDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class NotAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_anonymous


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'CUS'


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class StorePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        try:
            Designer.objects.get(customer_object__base_user=user)
        except:
            return False
        return True

    def has_object_permission(self, request, view, obj: Store):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        try:
            designer = Designer.objects.get(customer_object__base_user=user)
        except:
            return False
        return obj.designer == designer


class AddressPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        user = request.user
        try:
            customer = Customer.objects.get(base_user=user)
        except:
            return False
        return str(customer.id) == view.kwargs.get('customer_pk')

    def has_object_permission(self, request, view, obj: Address):
        user = request.user
        try:
            customer = Customer.objects.get(base_user=user)
        except:
            return False
        return obj.customer == customer
