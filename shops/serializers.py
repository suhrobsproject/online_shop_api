from rest_framework import serializers
from django.utils.text import slugify
from .models import Shop

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id', 'seller', 'name', 'slug', 'logo', 'is_verified', 'created_at')
        read_only_fields = ('seller', 'slug', 'is_verified', 'created_at')

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Do‘kon nomi kamida 3 ta belgidan iborat bo‘lishi kerak.")
        
        generated_slug = slugify(value)
        qs = Shop.objects.filter(slug=generated_slug)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
            
        if qs.exists():
            raise serializers.ValidationError("Bu nomdagi do‘kon allaqachon mavjud.")
            
        return value

