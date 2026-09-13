from django.urls import path
from .views import (
    CustomerOrderListCreateAPIView, CustomerOrderDetailAPIView,
    SellerOrderListAPIView, SellerOrderDetailAPIView, SellerOrderItemListAPIView
)

app_name = 'orders'

urlpatterns = [
    path('my-orders/', CustomerOrderListCreateAPIView.as_view(), name='customer-orders-list'),
    path('my-orders/<int:pk>/', CustomerOrderDetailAPIView.as_view(), name='customer-order-detail'),
    
    path('seller/orders/', SellerOrderListAPIView.as_view(), name='seller-orders-list'),
    path('seller/orders/<int:pk>/', SellerOrderDetailAPIView.as_view(), name='seller-order-detail'),
    path('seller/order-items/', SellerOrderItemListAPIView.as_view(), name='seller-order-items'),
]