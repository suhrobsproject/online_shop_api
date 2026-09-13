from rest_framework import serializers
from .models import Category, Product, ProductVariant, ProductImage
from backend.shops.models import Shop

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'slug', 'parent')

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'is_main', 'variant')

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ('id', 'attributes', 'price', 'old_price', 'stock')

class ProductListSerializer(serializers.ModelSerializer):
    category_title = serializers.CharField(source='category.title', read_only=True)
    shop_title = serializers.CharField(source='shop.title', read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'slug', 'category', 'category_title', 'shop', 'shop_title', 'description', 'images', 'variants', 'created_at')

class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, required=False)
    
    class Meta:
        model = Product
        fields = ('id', 'title', 'slug', 'category', 'shop', 'description', 'variants')

    def validate_shop(self, value):
        user = self.context['request'].user
        if not user.shops.filter(id=value.id, is_verified=True).exists():
            raise serializers.ValidationError("This shop does not belong to you or is not verified.")
        return value

    def create(self, validated_data):
        variants_data = validated_data.pop('variants', [])
        product = Product.objects.create(**validated_data)
        for variant_data in variants_data:
            ProductVariant.objects.create(product=product, **variant_data)
        return product

    def update(self, instance, validated_data):
        variants_data = validated_data.pop('variants', [])
        instance.title = validated_data.get('title', instance.title)
        instance.category = validated_data.get('category', instance.category)
        instance.shop = validated_data.get('shop', instance.shop)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        
        # This is a naive update: deletes all old variants and creates new ones.
        if 'variants' in self.initial_data:
            instance.variants.all().delete()
            for variant_data in variants_data:
                ProductVariant.objects.create(product=instance, **variant_data)
                
        return instance

