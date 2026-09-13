from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductVariantSerializer

class CartItemSerializer(serializers.ModelSerializer):
    variant_detail = ProductVariantSerializer(source='variant', read_only=True)
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'variant', 'variant_detail', 'quantity', 'subtotal')
        
    def validate(self, attrs):
        variant = attrs.get('variant')
        quantity = attrs.get('quantity', 1)
        if variant and quantity > variant.stock:
            raise serializers.ValidationError(f"Only {variant.stock} items are in stock.")
        return attrs

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    total_quantity = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'user', 'session_key', 'items', 'total_price', 'total_quantity')

