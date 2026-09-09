from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomUser(AbstractUser, BaseModel):

    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
    role = models.CharField(max_length=20, default='customer')
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
    ) # Gender qo'shish sababi saytga kirganda shunga qarab mahsulot taklif qilish uchun 

    
    USERNAME_FIELD = 'phone_number'  #Saytga nima bilan kiriladi

    REQUIRED_FIELDS = [] #REQUIRED_FIELDS esa — "Admin yaratishda telefondan tashqari yana nimalarni kiritish shart

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