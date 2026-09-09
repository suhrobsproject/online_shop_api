from django.urls import path
from .views import (
    ShopCreateView,
    ShopUpdateView,
    ShopDetailView,
    MyShopsListView,
    ShopDeleteView,
)

app_name = 'shops'

urlpatterns = [
    path('my-shops/', MyShopsListView.as_view(), name='my_shops'),
    path('create/', ShopCreateView.as_view(), name='create'),
    path('<slug:slug>/', ShopDetailView.as_view(), name='detail'),
    path('<slug:slug>/edit/', ShopUpdateView.as_view(), name='edit'),
    path('<slug:slug>/delete/', ShopDeleteView.as_view(), name='delete'),
]