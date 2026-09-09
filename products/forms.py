from django import forms
from django.forms import inlineformset_factory
from .models import Category, Product, ProductVariant, ProductImage


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('shop', 'category', 'title', 'description')
        widgets = {
            'shop': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mahsulot nomi'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Mahsulot haqida batafsil...'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Sotuvchi faqat o'ziga tegishli do'konlarni tanlay olishi uchun filtr
        if user is not None:
            self.fields['shop'].queryset = user.shops.all()


class ProductVariantForm(forms.ModelForm):
    custom_attributes = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': "Har bir qatorga bitta xususiyat yozing:\nRAM: 16 GB\nHDD: 512 GB SSD\nRang: Qora"
        }),
        required=False,
        label="Xususiyatlar (Atributlar)",
        help_text="Format: Nom: Qiymat (har biri yangi qatorda)"
    )

    class Meta:
        model = ProductVariant
        fields = ('price', 'old_price', 'stock')
        widgets = {
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Narxi'}),
            'old_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Eski narxi'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ombordagi soni'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Baza ichidagi JSON ma'lumotni tahrirlashda yana oddiy matn ko'rinishida chiqarib berish
        if self.instance and self.instance.pk and self.instance.attributes:
            lines = [f"{key}: {value}" for key, value in self.instance.attributes.items()]
            self.fields['custom_attributes'].initial = "\n".join(lines)

    def clean_custom_attributes(self):
        data = self.cleaned_data.get('custom_attributes', '').strip()
        if not data:
            return {}

        attributes_dict = {}
        # Har bir qatorni ajratib, lug'at (dict) hosil qilamiz
        for line in data.splitlines():
            line = line.strip()
            if not line:
                continue

            if ':' not in line:
                raise ValidationError(f"Noto‘g‘ri format: '{line}'. Iltimos, 'Nomi: Qiymati' ko‘rinishida yozing.")

            key, value = line.split(':', 1)
            key = key.strip().lower()  # Masalan: "ram", "hdd", "rang"
            value = value.strip()
            
            if key and value:
                attributes_dict[key] = value

        return attributes_dict

    def save(self, commit=True):
        variant = super().save(commit=False)
        # Tozalangan lug'atni to'g'ridan-to'g'ri modelning JSONField maydoniga yozamiz
        variant.attributes = self.cleaned_data.get('custom_attributes', {})
        if commit:
            variant.save()
        return variant

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ('image', 'is_main')
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_main': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# Mahsulot bilan birga variantlar va rasmlarni bitta formda saqlash uchun formsetlar
ProductVariantFormSet = inlineformset_factory(
    Product, ProductVariant, form=ProductVariantForm, extra=1, can_delete=True
)

ProductImageFormSet = inlineformset_factory(
    Product, ProductImage, form=ProductImageForm, extra=2, can_delete=True
)