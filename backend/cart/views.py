from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import ProductVariant

def _get_or_create_cart(request):
    if not request.session.session_key:
        request.session.create()

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)

    return cart

class CartAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        cart = _get_or_create_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class CartItemAddAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        cart = _get_or_create_cart(request)
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            variant = serializer.validated_data['variant']
            quantity = serializer.validated_data['quantity']
            
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                variant=variant,
                defaults={'quantity': quantity}
            )
            
            if not created:
                if cart_item.quantity + quantity > variant.stock:
                    return Response({"detail": f"Only {variant.stock} items are in stock."}, status=status.HTTP_400_BAD_REQUEST)
                cart_item.quantity += quantity
                cart_item.save(update_fields=['quantity'])
            
            return Response(CartSerializer(cart).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartItemUpdateDeleteAPIView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, pk):
        cart = _get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, pk=pk, cart=cart)
        serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            new_quantity = serializer.validated_data.get('quantity', cart_item.quantity)
            if new_quantity > cart_item.variant.stock:
                return Response({"detail": f"Only {cart_item.variant.stock} items are in stock."}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(CartSerializer(cart).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        return self.put(request, pk)

    def delete(self, request, pk):
        cart = _get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, pk=pk, cart=cart)
        cart_item.delete()
        return Response({"detail": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)