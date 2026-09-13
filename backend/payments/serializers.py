from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'order', 'provider', 'amount', 'status', 'transaction_id', 'created_at')
        read_only_fields = ('amount', 'status', 'transaction_id', 'created_at')

class PaymentMethodSerializer(serializers.Serializer):
    provider = serializers.ChoiceField(choices=Payment.ProviderChoices.choices)

class PaymentProcessSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=True, help_text="Set true to simulate successful payment.")

