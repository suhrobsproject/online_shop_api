from django.db import models
from django.conf import settings
from decimal import Decimal

from shops.models import BaseModel, Shop
from products.models import ProductVariant
from users.models import Address


class Order(BaseModel):
    class StatusChoices(models.TextChoices):
        PENDING = 'pending', 'Kutilmoqda'
        PAID = 'paid', 'To‘langan'
        PROCESSING = 'processing', 'Jarayonda'
        SHIPPED = 'shipped', 'Yo‘lda'
        DELIVERED = 'delivered', 'Yetkazib berildi'
        CANCELLED = 'cancelled', 'Bekor qilingan'

    # user_id (bigint)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="Buyurtmachi"
    )

    # status (varchar)
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        verbose_name="Holati"
    )

    # total_price (decimal)
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Umumiy summa"
    )

    # adress_id (bigint) -> Manzil o'chirilsa ham buyurtma tarixi saqlanib qolishi uchun SET_NULL
    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name="Yetkazib berish manzili"
    )

    class Meta:
        db_table = 'order'
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
        ordering = ['-created_at']

    def __str__(self):
        return f"Buyurtma #{self.id} - {self.user}"


class OrderItem(BaseModel):
    # order_id (bigint)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Buyurtma"
    )

    # variant_id (bigint)
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT,  # Buyurtma qilingan tovar bazadan tasodifan o'chib ketmasligi uchun
        related_name='order_items',
        verbose_name="Mahsulot varianti"
    )

    # shop_id (bigint) -> Sotuvchi o'z do'koniga tushgan tovarlarni alohida filtrlab ko'rishi uchun
    shop = models.ForeignKey(
        Shop,
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name="Do‘kon"
    )

    # quantity (bigint)
    quantity = models.PositiveBigIntegerField(
        default=1,
        verbose_name="Miqdori"
    )

    # price (decimal) -> Sotilgan paytdagi narxni muzlatib qo'yish uchun
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Sotilgan narxi"
    )

    class Meta:
        db_table = 'order_item'
        verbose_name = "Buyurtma tarkibi"
        verbose_name_plural = "Buyurtma tarkiblari"

    def __str__(self):
        return f"{self.variant} ({self.quantity} dona)"

    @property
    def subtotal(self):
        return self.price * self.quantity