from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_nested.routers import NestedDefaultRouter

router = DefaultRouter()
router.register('users', BaseUserViewSet, basename='base_users')
router.register('customers', CustomerViewSet, basename='customers')
router.register('admins', AdminViewSet, basename='admins')
router.register('providers', ProviderViewSet, basename='providers')
router.register('designers', DesignerViewSet, basename='designers')
router.register('stores', StoreManagerView, basename='stores')
router.register('addresses', AddressManagerView, basename='addresses')
router.register('my_addresses', AddressViewSet, basename='my_addresses')
designer_nested_router = NestedDefaultRouter(router, 'designers', lookup='designer')
designer_nested_router.register('stores', StoreViewSet, basename='stores')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(designer_nested_router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterCustomerView.as_view(), name='register'),
    path('add-admin/', AddAdminView.as_view(), name='add_admin'),
    path('add-provider/', AddProviderView.as_view(), name='add_admin'),
    path('get_my_info/', GetUserInfoView.as_view(), name='get_user_info'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('promote_to_designer/', promote_customer_to_designer, name='promote_to_designer'),
]
