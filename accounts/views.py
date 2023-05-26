from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import NotFound, AuthenticationFailed
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from django.shortcuts import get_object_or_404
from accounts.filters import BaseUserFilter, AdminFilter, DesignerFilter, ProviderFilter, AddressFilter, StoreFilter
from accounts.models import *
from accounts.permissons import MappedDjangoModelPermissions, NotAuthenticated, IsSuperUser, StorePermission, \
    IsAuthenticated, IsCustomer, AddressPermission
from accounts.serializers import *


class RegisterCustomerView(CreateAPIView):
    queryset = BaseUser.objects.all()
    serializer_class = RegisterCustomerSerializer
    permission_classes = (NotAuthenticated,)


class BaseUserViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):
    permission_classes = (MappedDjangoModelPermissions,)

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
        user = self.get_queryset().filter(id=pk).first()
        if not user:
            return Response({'message': "User not found"}, status=status.HTTP_404_NOT_FOUND)
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
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProviderFilter
    search_fields = ['name', ]
    ordering_fields = ['rate', ]
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
        designer = get_object_or_404(Designer, id=pk)
        if designer.is_premium:
            response = {'message': 'designer account is already premium'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        designer.is_premium = True
        designer.save()
        # some stuff happens here
        response = {'message': 'designer promoted successfully'}
        return Response(response, status=status.HTTP_200_OK)


class StoreManagerView(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       GenericViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = StoreFilter
    search_fields = ['store_name', ]
    permission_classes = (MappedDjangoModelPermissions,)


class StoreViewSet(StoreManagerView, mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin, mixins.CreateModelMixin):
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
        return {'request': self.request,
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


class ChangePasswordView(UpdateAPIView):
    queryset = BaseUser.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class AddressManagerView(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         GenericViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, ]
    filterset_class = AddressFilter
    search_fields = ['detail', 'phone_number']
    permission_classes = (MappedDjangoModelPermissions,)


class AddressViewSet(AddressManagerView, mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin, mixins.CreateModelMixin):
    permission_classes = (AddressPermission,)

    def get_queryset(self):
        customer_id = self.kwargs.get('customer_pk')
        customer_addresses = Address.objects.filter(customer_id=customer_id)
        return customer_addresses

    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'create':
            return SaveAddressSerializer
        else:
            return AddressSerializer

    def get_serializer_context(self):
        return {'request': self.request,
                'address_id': self.kwargs.get('pk')}


@api_view(['POST', ], )
@transaction.atomic
@permission_classes([IsCustomer])
def promote_customer_to_designer(request):
    user = request.user
    card_number = request.data.get('card_number')
    if card_number is None:
        response = {'missing field': 'card number'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    user.role = 'DES'
    user.save()
    designer = Designer.objects.create(card_number=card_number, customer_object=Customer.objects.get(base_user=user))
    serializer = DesignerSerializer(designer)
    return Response(serializer.data, status=status.HTTP_200_OK)
