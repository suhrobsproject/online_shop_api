from decimal import Decimal
from django.db import models
from django.conf import settings
from shops.models import BaseModel
from products.models import ProductVariant


class Cart(BaseModel):
    # user_id (bigint) - ro'yxatdan o'tganlar uchun, anonimlar uchun null bo'lishi mumkin
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='carts',
        verbose_name="Foydalanuvchi"
    )
    # session_key (varchar) - anonim foydalanuvchilar savatini aniqlash uchun
    session_key = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        db_index=True,
        verbose_name="Sessiya kaliti"
    )

    class Meta:
        db_table = 'cart'
        verbose_name = "Savatcha"
        verbose_name_plural = "Savatchalar"

    def __str__(self):
        if self.user:
            return f"{self.user} savatchasi"
        return f"Anonim savatcha ({self.session_key})"

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(BaseModel):
    # cart_id (bigint)
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Savatcha"
    )
    # variant_id (bigint)
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name="Mahsulot varianti"
    )
    # quantity (bigint)
    quantity = models.PositiveBigIntegerField(
        default=1,
        verbose_name="Miqdori"
    )

    class Meta:
        db_table = 'cart_items'
        verbose_name = "Savatchadagi tovar"
        verbose_name_plural = "Savatchadagi tovarlar"
        unique_together = ('cart', 'variant')  # Bitta savatda ayni bir variant ikki marta alohida qator bo'lib tushmasligi uchun

    def __str__(self):
        return f"{self.variant} ({self.quantity} dona)"

    @property
    def subtotal(self):
        return self.variant.price * self.quantity