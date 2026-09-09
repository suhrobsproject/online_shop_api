import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction

from .models import Payment
from .forms import PaymentMethodForm
from orders.models import Order


class PaymentCheckoutView(LoginRequiredMixin, View):
    """Buyurtma uchun to'lov turini tanlash sahifasi"""
    template_name = 'payments/payment_checkout.html'

    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id, user=request.user)
        
        # Agar buyurtma allaqachon to'langan bo'lsa
        if order.status == Order.StatusChoices.PAID:
            messages.info(request, "Ushbu buyurtma uchun to‘lov allaqachon amalga oshirilgan.")
            return redirect('orders:customer_order_detail', pk=order.pk)

        form = PaymentMethodForm()
        return render(request, self.template_name, {
            'order': order,
            'form': form
        })

    def post(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id, user=request.user)
        form = PaymentMethodForm(request.POST)

        if form.is_valid():
            provider = form.cleaned_data['provider']

            # Yangi to'lov yozuvini yaratish
            payment = Payment.objects.create(
                order=order,
                provider=provider,
                amount=order.total_price,
                status=Payment.StatusChoices.PENDING
            )

            # Agar naqd pul tanlansa, darhol qayta yo'naltiramiz
            if provider == Payment.ProviderChoices.CASH:
                payment.status = Payment.StatusChoices.PENDING
                payment.save(update_fields=['status'])
                messages.success(request, "Buyurtmangiz qabul qilindi. Mahsulot yetkazilganda to‘lov qilasiz.")
                return redirect('orders:customer_order_detail', pk=order.pk)

            # Onlayn to'lov sahifasiga yo'naltirish
            return redirect('payments:process', payment_id=payment.pk)

        return render(request, self.template_name, {'order': order, 'form': form})


class PaymentProcessView(LoginRequiredMixin, View):
    """To'lovni tasdiqlash sahifasi (integratsiyagacha test qilish uchun)"""
    template_name = 'payments/payment_process.html'

    def get(self, request, payment_id):
        payment = get_object_or_404(Payment, pk=payment_id, order__user=request.user)
        return render(request, self.template_name, {'payment': payment})

    def post(self, request, payment_id):
        payment = get_object_or_404(Payment, pk=payment_id, order__user=request.user)

        # Test to'lovini muvaffaqiyatli yakunlash simulyatsiyasi
        with transaction.atomic():
            payment.status = Payment.StatusChoices.SUCCESS
            payment.transaction_id = str(uuid.uuid4())[:18].upper()
            payment.save(update_fields=['status', 'transaction_id'])

            # Buyurtma holatini 'PAID' ga o'zgartirish
            order = payment.order
            order.status = Order.StatusChoices.PAID
            order.save(update_fields=['status'])

        messages.success(request, f"To‘lov muvaffaqiyatli amalga oshirildi! Tranzaksiya ID: {payment.transaction_id}")
        return redirect('orders:customer_order_detail', pk=payment.order.pk)