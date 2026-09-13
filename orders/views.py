from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import F
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer, OrderStatusUpdateSerializer, OrderItemSerializer
from cart.models import CartItem

class CustomerOrderListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]


    def get(self, request):
        orders = Order.objects.filter(user=request.user).prefetch_related('items__variant__product', 'items__shop')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        cart_items = CartItem.objects.filter(cart__user=request.user).select_related('variant__product__shop')
        if not cart_items.exists():
            return Response({"detail": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            for item in cart_items:
                if item.variant.stock < item.quantity:
                    return Response({"detail": f"Not enough stock for '{item.variant.product.title}' (Available: {item.variant.stock})."}, status=status.HTTP_400_BAD_REQUEST)

            order = Order.objects.create(
                user=request.user,
                address=serializer.validated_data.get('address'),
                payment_method=serializer.validated_data.get('payment_method')
            )

            total = 0
            for item in cart_items:
                item_price = item.variant.price
                OrderItem.objects.create(
                    order=order,
                    variant=item.variant,
                    shop=item.variant.product.shop,
                    quantity=item.quantity,
                    price=item_price
                )
                total += item_price * item.quantity
                
                item.variant.stock = F('stock') - item.quantity
                item.variant.save(update_fields=['stock'])

            order.total_price = total
            order.save(update_fields=['total_price'])
            cart_items.delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

class CustomerOrderDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        order = get_object_or_404(Order.objects.prefetch_related('items__variant__product', 'items__shop'), pk=pk, user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data)


class SellerOrderListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]


    def get(self, request):
        orders = Order.objects.filter(items__shop__seller=request.user).distinct()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class SellerOrderDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk, items__shop__seller=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk):
        order = get_object_or_404(Order, pk=pk, items__shop__seller=request.user)
        serializer = OrderStatusUpdateSerializer(order, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_order = serializer.save()

        if updated_order.status == Order.StatusChoices.CANCELLED:
            with transaction.atomic():
                for item in updated_order.items.all():
                    item.variant.stock = F('stock') + item.quantity
                    item.variant.save(update_fields=['stock'])

        return Response(OrderSerializer(updated_order).data)

    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk, items__shop__seller=request.user)
        serializer = OrderStatusUpdateSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_order = serializer.save()

        if updated_order.status == Order.StatusChoices.CANCELLED:
            with transaction.atomic():
                for item in updated_order.items.all():
                    item.variant.stock = F('stock') + item.quantity
                    item.variant.save(update_fields=['stock'])

        return Response(OrderSerializer(updated_order).data)


class SellerOrderItemListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]


    def get(self, request):
        items = OrderItem.objects.filter(shop__seller=request.user).select_related('order', 'variant__product')
        serializer = OrderItemSerializer(items, many=True)
        return Response(serializer.data)