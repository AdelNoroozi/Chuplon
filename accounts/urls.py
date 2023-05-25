from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('users', BaseUserViewSet, basename='BaseUser')
router.register('customers', CustomerViewSet, basename='Customer')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair_view'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh_view'),
    path('register/', RegisterCustomerView.as_view(), name='register'),
    path('add-admin/', AddAdminView.as_view(), name='add_admin'),
]
