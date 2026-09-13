from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterAPIView,
    ProfileAPIView,
    ChangePasswordAPIView,
    AddressListAPIView,
    AddressDetailAPIView
)

app_name = 'users'

urlpatterns = [
    # Auth
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Profile
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('password-change/', ChangePasswordAPIView.as_view(), name='password_change'),
    
    # Addresses
    path('addresses/', AddressListAPIView.as_view(), name='address_list'),
    path('addresses/<int:pk>/', AddressDetailAPIView.as_view(), name='address_detail'),
]