from django.urls import path
from .views import (
    OrderCreateView,
    CustomerOrderListView,
    CustomerOrderDetailView,
    SellerOrderListView,
    SellerOrderStatusUpdateView,
)

app_name = 'orders'

urlpatterns = [
    # Xaridor yo'nalishlari
    path('checkout/', OrderCreateView.as_view(), name='order_create'),
    path('my-orders/', CustomerOrderListView.as_view(), name='customer_orders'),
    path('my-orders/<int:pk>/', CustomerOrderDetailView.as_view(), name='customer_order_detail'),

    # Sotuvchi yo'nalishlari
    path('seller/orders/', SellerOrderListView.as_view(), name='seller_orders'),
    path('seller/orders/<int:pk>/status/', SellerOrderStatusUpdateView.as_view(), name='seller_order_status'),
]