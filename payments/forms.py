from django import forms
from .models import Payment


class PaymentMethodForm(forms.Form):
    provider = forms.ChoiceField(
        choices=Payment.ProviderChoices.choices,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label="To‘lov turini tanlang"
    )