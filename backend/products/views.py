from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Category, Product, ProductImage
from .serializers import CategorySerializer, ProductListSerializer, ProductCreateUpdateSerializer, ProductImageSerializer

class IsSellerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.role in ['seller', 'admin']

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.shop.seller == request.user


class CategoryListAPIView(APIView):
    permission_classes = [permissions.AllowAny]


    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class CategoryDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


class ProductListAPIView(APIView):
    permission_classes = [IsSellerOrReadOnly]

    def get_queryset(self):
        qs = Product.objects.select_related('shop', 'category').prefetch_related('images', 'variants')
        if not (self.request.user.is_authenticated and self.request.user.role == 'admin'):
            qs = qs.filter(shop__is_verified=True)
        return qs


    def get(self, request):
        qs = self.get_queryset()
        category = request.query_params.get('category')
        shop = request.query_params.get('shop')
        search = request.query_params.get('search')
        if category: qs = qs.filter(category_id=category)
        if shop: qs = qs.filter(shop_id=shop)
        if search: qs = qs.filter(title__icontains=search)
        
        serializer = ProductListSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductCreateUpdateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailAPIView(APIView):
    permission_classes = [IsSellerOrReadOnly]

    def get_object(self, slug):
        qs = Product.objects.select_related('shop', 'category').prefetch_related('images', 'variants')
        if not (self.request.user.is_authenticated and self.request.user.role == 'admin'):
            qs = qs.filter(shop__is_verified=True)
        obj = get_object_or_404(qs, slug=slug)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, slug):
        obj = self.get_object(slug)
        serializer = ProductListSerializer(obj)
        return Response(serializer.data)

    def put(self, request, slug):
        obj = self.get_object(slug)
        serializer = ProductCreateUpdateSerializer(obj, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, slug):
        obj = self.get_object(slug)
        serializer = ProductCreateUpdateSerializer(obj, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        obj = self.get_object(slug)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductImageListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]


    def get(self, request):
        images = ProductImage.objects.filter(product__shop__seller=request.user)
        serializer = ProductImageSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductImageSerializer(data=request.data)
        if serializer.is_valid():
            product_id = request.data.get('product')
            if not product_id:
                return Response({"product": "This field is required."}, status=status.HTTP_400_BAD_REQUEST)
            product = get_object_or_404(Product, id=product_id)
            if product.shop.seller != request.user:
                return Response({"detail": "You can only add images to your own products."}, status=status.HTTP_403_FORBIDDEN)
            serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductImageDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        obj = get_object_or_404(ProductImage, pk=pk, product__shop__seller=self.request.user)
        return obj

    def get(self, request, pk):
        obj = self.get_object(pk)
        serializer = ProductImageSerializer(obj)
        return Response(serializer.data)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)