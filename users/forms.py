import re
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, get_user_model
from .models import CustomUser, Address


CustomUser = get_user_model()


class CustomUserRegisterForm(forms.ModelForm):
    # 'role' maydoni bu yerdan olib tashlandi
    phone_number = forms.CharField(
        max_length=20,
        label="Telefon raqam",
        initial="+998",
        widget=forms.TextInput(attrs={
            'id': 'phone-mask-register',
            'placeholder': '+998 (__) ___-__-__'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Kamida 8 ta belgi'}),
        label="Parol"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Parolni qayta kiriting'}),
        label="Parolni tasdiqlang"
    )

    class Meta:
        model = CustomUser
        # 'role' maydoni fields ro'yxatidan olib tashlandi
        fields = ('phone_number', 'email')

    def clean_phone_number(self):
        raw_phone = self.cleaned_data.get('phone_number', '')
        clean_phone = re.sub(r'[^\d+]', '', raw_phone)

        if clean_phone.startswith('998'):
            clean_phone = '+' + clean_phone
        elif len(clean_phone) == 9 and not clean_phone.startswith('+'):
            clean_phone = '+998' + clean_phone

        if len(clean_phone) != 13 or not clean_phone.startswith('+998'):
            raise ValidationError("Telefon raqami noto‘g‘ri formatda kiritildi.")

        # Raqam oldin ro'yxatdan o'tmaganini tekshirish
        if CustomUser.objects.filter(phone_number=clean_phone).exists():
            raise ValidationError("Bu telefon raqam allaqachon ro‘yxatdan o‘tgan.")

        return clean_phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            return None  # Bo'sh satr o'rniga None qaytarish (IntegrityError ning oldini oladi)
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Ushbu email allaqachon band.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if not password:
            return cleaned_data

        if len(password) < 8:
            self.add_error('password', "Parol kamida 8 ta belgidan iborat bo‘lsin.")

        if password.isdigit():
            self.add_error('password', "Parol faqat sonlardan iborat bo‘lmasin.")

        if not confirm_password:
            self.add_error('confirm_password', "Parolni tasdiqlash maydonini to‘ldiring.")
        elif password != confirm_password:
            self.add_error('confirm_password', "Parollar bir-biriga mos kelmadi!")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Login ishlashi uchun username ga ham telefon raqam o'rnatiladi
        user.username = self.cleaned_data["phone_number"]
        user.set_password(self.cleaned_data["password"])
        
        # Har bir ro'yxatdan o'tgan foydalanuvchiga avtomatik 'customer' roli beriladi
        user.role = 'customer'

        if commit:
            user.save()
        return user

    
class CustomUserLoginForm(forms.Form):
    phone_number = forms.CharField(
        max_length=20,
        label="Telefon raqam",
        initial="+998",
        widget=forms.TextInput(attrs={
            'id': 'phone-mask-login',
            'placeholder': '+998 (__) ___-__-__'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Parol"
    )

    def clean_phone_number(self):
        raw_phone = self.cleaned_data.get('phone_number', '')
        clean_phone = re.sub(r'[^\d+]', '', raw_phone)

        if clean_phone.startswith('998'):
            clean_phone = '+' + clean_phone
        elif len(clean_phone) == 9 and not clean_phone.startswith('+'):
            clean_phone = '+998' + clean_phone

        if len(clean_phone) != 13 or not clean_phone.startswith('+998'):
            raise ValidationError("Telefon raqami noto‘g‘ri formatda kiritildi.")

        return clean_phone

    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get('phone_number')
        password = cleaned_data.get('password')

        if phone_number and password:
            # clean_phone_number dan o'tgan toza raqam username sifatida beriladi
            self.user = authenticate(username=phone_number, password=password)

            if self.user is None:
                raise ValidationError("Telefon raqam yoki parol noto‘g‘ri kiritildi.")

            if not self.user.is_active:
                raise ValidationError("Foydalanuvchi hisobi faol emas.")

        return cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)



class CustomUserProfileForm(forms.ModelForm):
    # Telefon va rolni faqat ko'rsatish uchun bloklangan (disabled) qilib chiqaramiz
    phone_number = forms.CharField(
        label="Telefon raqam",
        disabled=True,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control bg-light', 'readonly': 'readonly'})
    )
    role = forms.CharField(
        label="Foydalanuvchi maqomi",
        disabled=True,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control bg-light', 'readonly': 'readonly'})
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'gender', 'phone_number', 'role')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ismingiz'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Familiyangiz'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.com'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agar foydalanuvchi mavjud bo'lsa, rolning inglizcha kodini emas, o'zbekcha chiroyli nomini chiqaramiz
        if self.instance and self.instance.pk:
            self.fields['role'].initial = self.instance.get_role_display() if hasattr(self.instance, 'get_role_display') else self.instance.role

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            return None
        
        user_exists = CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists()
        if user_exists:
            raise ValidationError("Ushbu email boshqa hisob tomonidan band qilingan.")

        return email



class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ismingiz'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Familiyangiz'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'namuna@mail.com'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            return None  # Bo'sh qolsa bazaga bo'sh satr emas, NULL (None) tushishi uchun

        # O'zidan boshqa biror foydalanuvchi shu emailni band qilganmi-yo'qligini tekshirish
        email_exists = CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists()
        if email_exists:
            raise ValidationError("Ushbu email boshqa hisob tomonidan band qilingan.")

        return email


class CustomUserChangePasswordForm(forms.ModelForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Joriy parolingiz'}),
        label="Eski parol"
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Yangi parol'}),
        label="Yangi parol"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Yangi parolni tasdiqlang'}),
        label="Yangi parolni tasdiqlang"
    )

    class Meta:
        model = CustomUser
        fields = ()

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.instance.check_password(old_password):
            raise ValidationError("Eski parol noto‘g‘ri kiritildi.")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if not new_password:
            return cleaned_data

        if len(new_password) < 8:
            self.add_error('new_password', "Parol kamida 8 ta belgidan iborat bo‘lishi kerak.")

        if new_password.isdigit():
            self.add_error('new_password', "Parol faqat raqamlardan iborat bo‘lmasligi kerak.")

        if not confirm_password:
            self.add_error('confirm_password', "Yangi parolni tasdiqlash maydonini to‘ldiring.")
        elif new_password != confirm_password:
            self.add_error('confirm_password', "Yangi parollar bir-biriga mos kelmadi.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['new_password'])
        if commit:
            user.save()
        return user


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('region', 'city', 'street', 'house_number')
        widgets = {
            'region': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Viloyat'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shahar yoki tuman'}),
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ko‘cha nomi'}),
            'house_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Uy/xonadon raqami'}),
        }