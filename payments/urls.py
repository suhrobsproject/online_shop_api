from django.urls import path
from .views import PaymentCheckoutAPIView, PaymentProcessAPIView

app_name = 'payments'

urlpatterns = [
    path('checkout/<int:order_id>/', PaymentCheckoutAPIView.as_view(), name='checkout'),
    path('process/<int:payment_id>/', PaymentProcessAPIView.as_view(), name='process'),
]