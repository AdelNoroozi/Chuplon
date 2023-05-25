from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from accounts.models import *
from accounts.permissons import MappedDjangoModelPermissions
from accounts.serializers import *


class BaseUserViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):
    permission_classes = (MappedDjangoModelPermissions,)

    def get_serializer_class(self):
        if self.action == 'list':
            return BaseUserMiniSerializer
        else:
            return BaseUserSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return BaseUser.objects.all()
        elif self.request.user.is_staff:
            # admin = Admin.objects.get(base_user=self.request.user)
            # admins section must be checked here too
            return BaseUser.objects.filter(is_staff=False)
        else:
            return BaseUser.objects.none()
