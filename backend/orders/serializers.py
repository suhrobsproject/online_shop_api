from rest_framework import serializers
from .models import Order, OrderItem
from users.serializers import AddressSerializer
from cart.models import CartItem

class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='variant.product.title', read_only=True)
    shop_title = serializers.CharField(source='shop.title', read_only=True)
    variant_attributes = serializers.JSONField(source='variant.attributes', read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'variant', 'product_title', 'variant_attributes', 'shop', 'shop_title', 'quantity', 'price', 'subtotal')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    address_detail = AddressSerializer(source='address', read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'status', 'total_price', 'address', 'address_detail', 'payment_method', 'items', 'created_at')
        read_only_fields = ('user', 'status', 'total_price', 'created_at')


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('address', 'payment_method')

    def validate_address(self, value):
        user = self.context['request'].user
        if value.user != user:
            raise serializers.ValidationError("This address does not belong to you.")
        return value

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('status',)

