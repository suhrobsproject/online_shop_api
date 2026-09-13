from django.urls import path
from .views import ShopListAPIView, ShopDetailAPIView

app_name = 'shops'

urlpatterns = [
    path('', ShopListAPIView.as_view(), name='shop-list'),
    path('<slug:slug>/', ShopDetailAPIView.as_view(), name='shop-detail'),
]