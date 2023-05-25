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
designer_nested_router = NestedDefaultRouter(router, 'designers', lookup='designer')
designer_nested_router.register('stores', StoreViewSet, basename='stores')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(designer_nested_router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair_view'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh_view'),
    path('register/', RegisterCustomerView.as_view(), name='register'),
    path('add-admin/', AddAdminView.as_view(), name='add_admin'),
    path('add-provider/', AddProviderView.as_view(), name='add_admin'),
]
