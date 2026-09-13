from django.urls import path
from .views import CartAPIView, CartItemAddAPIView, CartItemUpdateDeleteAPIView

app_name = 'cart'

urlpatterns = [
    path('', CartAPIView.as_view(), name='cart-detail'),
    path('add/', CartItemAddAPIView.as_view(), name='cart-add'),
    path('items/<int:pk>/', CartItemUpdateDeleteAPIView.as_view(), name='cart-item-manage'),
]