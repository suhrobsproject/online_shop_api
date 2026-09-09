from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from .models import Shop


class ShopCreateForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ('name', 'logo')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masalan: Texnomart yoki JoyBox'
            }),
            'logo': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'name': 'Do‘kon nomi',
            'logo': 'Do‘kon logotipi (ixtiyoriy)'
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()

        if len(name) < 3:
            raise ValidationError("Do‘kon nomi kamida 3 ta belgidan iborat bo‘lishi kerak.")

        # Nomdan slug yasab, unikalligini tekshirish
        generated_slug = slugify(name)
        if Shop.objects.filter(slug=generated_slug).exists():
            raise ValidationError("Bu nomdagi do‘kon allaqachon mavjud. Boshqa nom tanlang.")

        return name


class ShopUpdateForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ('name', 'logo')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Do‘kon nomi',
            'logo': 'Yangi logotip yuklash'
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()

        if len(name) < 3:
            raise ValidationError("Do‘kon nomi kamida 3 ta belgidan iborat bo‘lishi kerak.")

        # Tahrirlashda o'zining joriy slug/nomini hisobga olmasdan tekshirish
        generated_slug = slugify(name)
        slug_exists = Shop.objects.filter(slug=generated_slug).exclude(pk=self.instance.pk).exists()
        if slug_exists:
            raise ValidationError("Bu nomdagi do‘kon allaqachon mavjud.")

        return name

    def save(self, commit=True):
        shop = super().save(commit=False)
        # Nom o'zgarganda slug ham avtomatik qayta generatsiya qilinadi
        shop.slug = slugify(shop.name)
        if commit:
            shop.save()
        return shop