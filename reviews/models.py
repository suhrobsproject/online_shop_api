from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from shops.models import BaseModel
from products.models import Product


class Comment(BaseModel):
    # user_id (bigint)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Foydalanuvchi"
    )
    # product_id (bigint)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Mahsulot"
    )
    # comment (varchar)
    comment = models.TextField(
        verbose_name="Sharh matni"
    )
    # rating (smallint: 1 dan 5 gacha)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Baho (1-5)"
    )

    class Meta:
        db_table = 'comments'
        verbose_name = "Sharh"
        verbose_name_plural = "Sharhlar"
        ordering = ['-created_at']
        unique_together = ('user', 'product')  # Bitta foydalanuvchi 1 ta mahsulotga faqat 1 ta sharh qoldiradi

    def __str__(self):
        return f"{self.user} - {self.product.title} ({self.rating}/5)"