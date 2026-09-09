from django.urls import path
from .views import PaymentCheckoutView, PaymentProcessView

app_name = 'payments'

urlpatterns = [
    path('checkout/<int:order_id>/', PaymentCheckoutView.as_view(), name='checkout'),
    path('process/<int:payment_id>/', PaymentProcessView.as_view(), name='process'),
]