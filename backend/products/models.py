from django.db import models
from django.utils.text import slugify
from shops.models import BaseModel, Shop


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name="Kategoriya nomi")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="Slug")
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="Asosiy kategoriya"
    )

    class Meta:
        db_table = 'categories'
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Product(BaseModel):
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Do‘kon"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Kategoriya"
    )
    title = models.CharField(max_length=255, verbose_name="Mahsulot nomi")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="Slug")
    description = models.TextField(blank=True, null=True, verbose_name="Tavsif")

    class Meta:
        db_table = 'product'
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants',
        verbose_name="Mahsulot"
    )
    # JSONB ustuni: rang, o'lcham, xotira hajmi kabi moslashuvchan parametrlar uchun
    # Masalan: {"color": "Qora", "size": "XL", "ram": "8GB"}
    attributes = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Atributlar"
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Narxi"
    )
    old_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Eski narxi (chegirma uchun)"
    )
    stock = models.BigIntegerField(
        default=0,
        verbose_name="Ombordagi soni"
    )

    class Meta:
        db_table = 'product_variants'
        verbose_name = "Mahsulot varianti"
        verbose_name_plural = "Mahsulot variantlari"

    def __str__(self):
        return f"{self.product.title} - {self.attributes}"


class ProductImage(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Mahsulot"
    )
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='images',
        verbose_name="Variant"
    )
    image = models.ImageField(
        upload_to='products/images/',
        verbose_name="Rasm"
    )
    is_main = models.BooleanField(
        default=False,
        verbose_name="Asosiy rasm"
    )

    class Meta:
        db_table = 'product_images'
        verbose_name = "Mahsulot rasmi"
        verbose_name_plural = "Mahsulot rasmlari"
        ordering = ['-is_main', '-created_at']

    def __str__(self):
        return f"{self.product.title} rasmi"