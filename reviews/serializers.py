from rest_framework import serializers
from .models import Comment
from products.models import Product
from orders.models import OrderItem, Order

class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.phone_number', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'user_name', 'product', 'comment', 'rating', 'created_at')
        read_only_fields = ('user', 'created_at')

    def validate(self, attrs):
        user = self.context['request'].user
        product = attrs.get('product')

        if Comment.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("Siz ushbu mahsulotga allaqachon sharh qoldirgansiz.")

        has_purchased = OrderItem.objects.filter(
            order__user=user,
            order__status=Order.StatusChoices.DELIVERED,
            variant__product=product
        ).exists()

        if not has_purchased:
            raise serializers.ValidationError("Sharh qoldirish uchun mahsulotni avval sotib olgan bo‘lishingiz kerak.")

        return attrs

