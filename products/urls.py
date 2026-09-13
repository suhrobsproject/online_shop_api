from django.urls import path
from .views import (
    CategoryListAPIView, CategoryDetailAPIView,
    ProductListAPIView, ProductDetailAPIView,
    ProductImageListAPIView, ProductImageDetailAPIView
)

app_name = 'products'

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    
    path('images/', ProductImageListAPIView.as_view(), name='product-image-list'),
    path('images/<int:pk>/', ProductImageDetailAPIView.as_view(), name='product-image-detail'),
    
    path('', ProductListAPIView.as_view(), name='product-list'),
    path('<slug:slug>/', ProductDetailAPIView.as_view(), name='product-detail'),
]