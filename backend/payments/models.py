from django.db import models

# Create your models here.
from django.db import models
from orders.models import Order


class Payment(models.Model):
    class ProviderChoices(models.TextChoices):
        CLICK = 'click', 'Click'
        PAYME = 'payme', 'Payme'
        UZUM = 'uzum', 'Uzum Bank'
        CASH = 'cash', 'Naqd pul (Yetkazilganda)'

    class StatusChoices(models.TextChoices):
        PENDING = 'pending', 'Kutilmoqda'
        SUCCESS = 'success', 'Muvaffaqiyatli'
        FAILED = 'failed', 'Xatolik'
        CANCELLED = 'cancelled', 'Bekor qilingan'

    # order_id (bigint)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name="Buyurtma"
    )

    # provider (varchar)
    provider = models.CharField(
        max_length=50,
        choices=ProviderChoices.choices,
        verbose_name="To‘lov tizimi"
    )

    # amount (decimal)
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="To‘lov summasi"
    )

    # status (varchar)
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        verbose_name="To‘lov holati"
    )

    # transaction_id (varchar)
    transaction_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
        verbose_name="Tranzaksiya ID (Tizim kodi)"
    )

    # created_at (timestamp)
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan vaqti"
    )

    class Meta:
        db_table = 'payments'
        verbose_name = "To‘lov"
        verbose_name_plural = "To‘lovlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"To‘lov #{self.id} - {self.provider} ({self.amount} so'm)"