from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Shop
from .serializers import ShopSerializer

class ShopListAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


    def get(self, request):
        if request.query_params.get('mine') == 'true' and request.user.is_authenticated:
            shops = Shop.objects.filter(seller=request.user)
        else:
            shops = Shop.objects.all()
        serializer = ShopSerializer(shops, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ShopSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(seller=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShopDetailAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_object(self, slug, for_update=False):
        if for_update:
            return get_object_or_404(Shop, slug=slug, seller=self.request.user)
        return get_object_or_404(Shop, slug=slug)

    def get(self, request, slug):
        shop = self.get_object(slug)
        serializer = ShopSerializer(shop)
        return Response(serializer.data)

    def put(self, request, slug):
        shop = self.get_object(slug, for_update=True)
        serializer = ShopSerializer(shop, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, slug):
        shop = self.get_object(slug, for_update=True)
        serializer = ShopSerializer(shop, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        shop = self.get_object(slug, for_update=True)
        user = request.user
        shop.delete()
        if not user.shops.exists():
            user.role = 'customer'
            user.save(update_fields=['role'])
        return Response(status=status.HTTP_204_NO_CONTENT)