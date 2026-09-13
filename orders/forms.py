from django import forms
from .models import Order
from users.models import Address


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('address', 'payment_method')
        widgets = {
            'address': forms.Select(attrs={'class': 'form-select'}),
            'payment_method': forms.RadioSelect(attrs={'class': 'form-check-input'})
        }
        labels = {
            'address': 'Yetkazib berish manzili',
            'payment_method': "To'lov usuli"
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Xaridor faqat o'ziga tegishli manzillarni ko'ra oladi
        if user is not None:
            self.fields['address'].queryset = Address.objects.filter(user=user)
            self.fields['address'].empty_label = "Manzilni tanlang"


class OrderStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('status',)
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'status': 'Buyurtma holati'
        }