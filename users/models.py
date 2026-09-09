from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True





class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Telefon raqami kiritilishi shart!")

        extra_fields.setdefault('role', 'customer')
        
        # username bo'sh qolmasligi yoki telefon raqami bilan to'ldirilishi uchun
        if not extra_fields.get('username'):
            extra_fields['username'] = phone_number

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuserda is_staff=True bo‘lishi kerak.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuserda is_superuser=True bo‘lishi kerak.")

        return self.create_user(phone_number, password, **extra_fields)


class CustomUser(AbstractUser, BaseModel):
    ROLE_CHOICES = (
        ('customer', 'Mijoz'),
        ('seller', 'Sotuvchi'),
        ('admin', 'Admin'),
    )

    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,  # get_role_display() ishlashi uchun kerak
        default='customer'
    )
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=20, unique=True)

    GENDER_CHOICES = (
        ('male', 'Erkak'),
        ('female', 'Ayol'),
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
        verbose_name="Jinsi"
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    # Standart managerni o'zgartiramiz:
    objects = CustomUserManager()

    class Meta:
        db_table = 'user'

    def __str__(self):
        return f"{self.phone_number} ({self.get_role_display()})"

    
class Address(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    region = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    house_number = models.CharField(max_length=200)