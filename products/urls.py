from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    SellerProductListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
)

app_name = 'products'

urlpatterns = [
    # Mijozlar uchun
    path('', ProductListView.as_view(), name='product_list'),
    path('detail/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),

    # Sotuvchi (Vendor) CRUD
    path('seller/my-products/', SellerProductListView.as_view(), name='seller_products'),
    path('seller/create/', ProductCreateView.as_view(), name='product_create'),
    path('seller/<slug:slug>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('seller/<slug:slug>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]