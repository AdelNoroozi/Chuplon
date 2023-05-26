from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, AuthenticationFailed
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from accounts.filters import BaseUserFilter, AdminFilter, DesignerFilter
from accounts.models import *
from accounts.permissons import MappedDjangoModelPermissions, NotAuthenticated, IsSuperUser, StorePermission
from accounts.serializers import *


class RegisterCustomerView(CreateAPIView):
    queryset = BaseUser.objects.all()
    serializer_class = RegisterCustomerSerializer
    permission_classes = (NotAuthenticated,)


class BaseUserViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):
    # permission_classes = (MappedDjangoModelPermissions,)

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BaseUserFilter
    search_fields = ['phone_number', 'first_name', 'last_name', 'username', 'email', ]
    ordering_fields = ['date_joined']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return BaseUser.objects.all()
        elif self.request.user.is_staff:
            return BaseUser.objects.filter(is_staff=False).exclude(role='PRP')
        else:
            return BaseUser.objects.none()

    def get_serializer_class(self):
        if self.action == 'list':
            return BaseUserMiniSerializer
        else:
            return BaseUserSerializer

    @classmethod
    def get_user_by_id(cls, _id):
        if BaseUser.objects.filter(id=_id).exists():
            return BaseUser.objects.get(id=_id)

    @action(detail=True, methods=['PATCH'])
    def change_activation_status(self, request, pk=None):
        user = BaseUserViewSet.get_user_by_id(_id=pk)
        if not user:
            return Response({'message': "User not found"}, status=status.HTTP_404_NOT_FOUND)
        if user not in self.get_queryset():
            raise NotFound("detail not found.")
        if user.is_superuser:
            return Response({'message': 'Cannot perform this action on a superuser'}, status=status.HTTP_403_FORBIDDEN)
        user.is_active = not user.is_active
        user.save()
        if user.is_active:
            response_message = 'Account activated successfully.'
        else:
            response_message = 'Account deactivated successfully.'
        return Response({'message': response_message}, status=status.HTTP_200_OK)


class AbstractAddUserTypeView(CreateAPIView):
    queryset = BaseUser.objects.all()
    permission_classes = (IsSuperUser,)


class AddAdminView(AbstractAddUserTypeView):
    serializer_class = AddAdminSerializer


class CustomerViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):
    queryset = Customer.objects.all()
    permission_classes = (MappedDjangoModelPermissions,)

    def get_serializer_class(self):
        if self.action == 'list':
            return CustomerMiniSerializer
        else:
            return CustomerSerializer


class AdminViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   GenericViewSet):
    queryset = Admin.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdminFilter
    permission_classes = (IsSuperUser,)

    def get_serializer_class(self):
        if self.action == 'list':
            return AdminMiniSerializer
        else:
            return AdminSerializer


class AddProviderView(AbstractAddUserTypeView):
    serializer_class = AddProviderSerializer


class ProviderViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):
    queryset = PrintProvider.objects.all()
    # filters
    permission_classes = (MappedDjangoModelPermissions,)

    def get_serializer_class(self):
        if self.action == 'list':
            return ProviderMiniSerializer
        else:
            return ProviderSerializer


class DesignerViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):
    queryset = Designer.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = DesignerFilter
    ordering_fields = ['promotion_date', 'balance']
    permission_classes = (MappedDjangoModelPermissions,)

    def get_serializer_class(self):
        if self.action == 'list':
            return DesignerMiniSerializer
        else:
            return DesignerSerializer

    @action(detail=True, methods=['PATCH'])
    def promote_to_premium(self, request, pk=None):
        if not Designer.objects.filter(id=pk).exists():
            response = {'message': 'designer not found'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        designer = Designer.objects.get(id=pk)
        if designer.is_premium:
            response = {'message': 'designer account is already premium'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        designer.is_premium = True
        designer.save()
        # some stuff happens here
        response = {'message': 'designer promoted successfully'}
        return Response(response, status=status.HTTP_200_OK)


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    filter_backends = [SearchFilter, ]
    search_fields = ['store_name', ]
    permission_classes = (StorePermission,)

    def get_queryset(self):
        designer_id = self.kwargs.get('designer_pk')
        designer_stores = Store.objects.filter(designer_id=designer_id)
        return designer_stores

    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'create':
            return SaveStoreSerializer
        else:
            return StoreSerializer

    def get_serializer_context(self):
        return {'designer_id': self.kwargs.get('designer_pk'),
                'store_id': self.kwargs.get('pk')}


class GetUserInfoView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            raise AuthenticationFailed('not authenticated')
        user = request.user
        if user.is_staff:
            serializer = BaseUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if user.role == 'CUS':
            customer = Customer.objects.get(base_user=user)
            serializer = CustomerSerializer(customer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if user.role == 'DES':
            designer = Designer.objects.get(customer_object__base_user=user)
            serializer = DesignerSerializer(designer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if user.role == 'PRP':
            provider = PrintProvider.objects.get(base_user=user)
            serializer = ProviderSerializer(provider)
            return Response(serializer.data, status=status.HTTP_200_OK)
