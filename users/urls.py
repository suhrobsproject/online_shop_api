from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    ProfileView,
    ChangePasswordView,
    AddressListView,
    AddressUpdateView,
    AddressDeleteView,
)

app_name = 'users'

urlpatterns = [
    # Autentifikatsiya
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Profil va xavfsizlik
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password-change/', ChangePasswordView.as_view(), name='change_password'),

    # Yetkazib berish manzillari
    path('addresses/', AddressListView.as_view(), name='address_list'),
    path('addresses/<int:pk>/edit/', AddressUpdateView.as_view(), name='address_update'),
    path('addresses/<int:pk>/delete/', AddressDeleteView.as_view(), name='address_delete'),
]