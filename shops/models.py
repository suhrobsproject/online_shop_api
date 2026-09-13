from django.db import models
from django.conf import settings
from django.utils.text import slugify


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan vaqti"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Yangilangan vaqti"
    )

    class Meta:
        abstract = True  # Ushbu model uchun ma'lumotlar bazasida jadval yaratilmaydi


class Shop(BaseModel):
    # seller_id (bigint) -> Bitta sotuvchi bir nechta do'kon ochishi mumkin
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shops',
        verbose_name="Sotuvchi"
    )

    # name (varchar)
    name = models.CharField(
        max_length=255,
        verbose_name="Do‘kon nomi"
    )

    # slug (varchar)
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        verbose_name="Slug"
    )

    # logo (varchar)
    logo = models.ImageField(
        upload_to='shops/logos/',
        blank=True,
        null=True,
        verbose_name="Do‘kon logotipi"
    )

    # is_verified (boolean)
    is_verified = models.BooleanField(
        default=False,
        verbose_name="Tasdiqlangan"
    )

    class Meta:
        db_table = 'shops'
        verbose_name = "Do‘kon"
        verbose_name_plural = "Do‘konlar"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
        # Do'kon tasdiqlansa, egasini sotuvchiga aylantiramiz
        if self.is_verified and self.seller.role != 'seller':
            self.seller.role = 'seller'
            self.seller.save(update_fields=['role'])
        # Agar do'kon tasdiqdan o'tmagan yoki bekor qilingan bo'lsa
        elif not self.is_verified and self.seller.role == 'seller':
            if not self.seller.shops.filter(is_verified=True).exclude(pk=self.pk).exists():
                self.seller.role = 'customer'
                self.seller.save(update_fields=['role'])