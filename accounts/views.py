from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from accounts.models import *
from accounts.permissons import MappedDjangoModelPermissions, NotAuthenticated
from accounts.serializers import *


class RegisterCustomerView(CreateAPIView):
    queryset = BaseUser.objects.all()
    serializer_class = RegisterCustomerSerializer
    permission_classes = (NotAuthenticated,)


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

    @classmethod
    def get_user_by_id(cls, _id):
        if BaseUser.objects.filter(id=_id).exists():
            return BaseUser.objects.get(id=_id)

    @action(detail=True, methods=['PATCH'])
    def change_activation_status(self, request, pk=None):
        user = BaseUserViewSet.get_user_by_id(_id=pk)
        if not user:
            return Response({'message': "User not found"}, status=status.HTTP_404_NOT_FOUND)
        if user.is_superuser:
            return Response({'message': 'Cannot perform this action on a superuser'}, status=status.HTTP_403_FORBIDDEN)
        # if user.is_staff and not request.user.is_superuser:
        #     return Response({'message': 'Only superusers can change the status of staff users'},
        #                     status=status.HTTP_403_FORBIDDEN)
        user.is_active = not user.is_active
        user.save()
        if user.is_active:
            response_message = 'Account activated successfully.'
        else:
            response_message = 'Account deactivated successfully.'
        return Response({'message': response_message}, status=status.HTTP_200_OK)
