from rest_framework.permissions import DjangoModelPermissions, BasePermission


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


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser