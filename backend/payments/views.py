import uuid
from rest_framework import views, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Payment
from orders.models import Order
from .serializers import PaymentSerializer, PaymentMethodSerializer, PaymentProcessSerializer


class PaymentCheckoutAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id, user=request.user)
        
        if order.status == Order.StatusChoices.PAID:
            return Response({"detail": "This order is already paid."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PaymentMethodSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider = serializer.validated_data['provider']

        payment = Payment.objects.create(
            order=order,
            provider=provider,
            amount=order.total_price,
            status=Payment.StatusChoices.PENDING
        )

        if provider == Payment.ProviderChoices.CASH:
            payment.status = Payment.StatusChoices.PENDING
            payment.save(update_fields=['status'])
            return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)

        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)


class PaymentProcessAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, payment_id):
        payment = get_object_or_404(Payment, pk=payment_id, order__user=request.user)
        serializer = PaymentProcessSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        success = serializer.validated_data.get('success', True)

        if success:
            with transaction.atomic():
                payment.status = Payment.StatusChoices.SUCCESS
                payment.transaction_id = str(uuid.uuid4())[:18].upper()
                payment.save(update_fields=['status', 'transaction_id'])

                order = payment.order
                order.status = Order.StatusChoices.PAID
                order.save(update_fields=['status'])
        else:
            payment.status = Payment.StatusChoices.FAILED
            payment.save(update_fields=['status'])

        return Response(PaymentSerializer(payment).data, status=status.HTTP_200_OK)