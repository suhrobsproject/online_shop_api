from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from django.db.models import F
from .models import Order, OrderItem
from .forms import OrderCreateForm, OrderStatusUpdateForm
from cart.models import CartItem  # Cart ilovangizdagi savatcha modeli bo'yicha


# ---------------- XARIDOR KO'RINISHI (CUSTOMER) ---------------- #

class OrderCreateView(LoginRequiredMixin, View):
    """
    Savatchadagi tovarlarni olib, Order va OrderItem larni yaratish,
    ombordan tovar qoldig'ini (stock) ayirish
    """
    template_name = 'orders/order_create.html'

    def get(self, request):
        cart_items = CartItem.objects.filter(cart__user=request.user).select_related('variant__product', 'variant__product__shop')
        if not cart_items.exists():
            messages.warning(request, "Savatchangiz bo'sh. Buyurtma berish uchun mahsulot tanlang.")
            return redirect('cart:cart_detail')

        form = OrderCreateForm(user=request.user)
        total_price = sum(item.variant.price * item.quantity for item in cart_items)

        return render(request, self.template_name, {
            'form': form,
            'cart_items': cart_items,
            'total_price': total_price
        })

    def post(self, request):
        cart_items = CartItem.objects.filter(cart__user=request.user).select_related('variant__product__shop')
        if not cart_items.exists():
            messages.warning(request, "Savatchangiz bo'sh.")
            return redirect('cart:cart_detail')

        form = OrderCreateForm(request.POST, user=request.user)
        if form.is_valid():
            with transaction.atomic():
                # Ombordagi qoldiqni tekshirish
                for item in cart_items:
                    if item.variant.stock < item.quantity:
                        messages.error(request, f"'{item.variant.product.title}' tovaridan omborda yetarli qolmagan (Mavjud: {item.variant.stock}).")
                        return redirect('cart:cart_detail')

                # Asosiy buyurtmani yaratish
                order = form.save(commit=False)
                order.user = request.user
                order.save()

                total = Decimal('0.00')
                for item in cart_items:
                    item_price = item.variant.price
                    # OrderItem larni saqlash
                    OrderItem.objects.create(
                        order=order,
                        variant=item.variant,
                        shop=item.variant.product.shop,
                        quantity=item.quantity,
                        price=item_price
                    )
                    total += item_price * item.quantity


                    # Ombordan ayirish                    
                    item.variant.stock = F('stock') - item.quantity
                    item.variant.save(update_fields=['stock'])


                order.total_price = total
                order.save(update_fields=['total_price'])

                # Savatchani tozalash
                cart_items.delete()

            messages.success(request, f"#{order.id} raqamli buyurtmangiz qabul qilindi!")
            return redirect('orders:customer_order_detail', pk=order.pk)

        return render(request, self.template_name, {'form': form, 'cart_items': cart_items})


class CustomerOrderListView(LoginRequiredMixin, View):
    """Xaridor o'z buyurtmalari ro'yxatini ko'rishi"""
    template_name = 'orders/customer_order_list.html'

    def get(self, request):
        orders = Order.objects.filter(user=request.user).prefetch_related('items__variant__product')
        return render(request, self.template_name, {'orders': orders})


class CustomerOrderDetailView(LoginRequiredMixin, View):
    """Xaridor bitta buyurtmasining to'liq tafsilotini ko'rishi"""
    template_name = 'orders/customer_order_detail.html'

    def get(self, request, pk):
        order = get_object_or_404(
            Order.objects.prefetch_related('items__variant__product', 'items__shop').select_related('address'),
            pk=pk,
            user=request.user
        )
        return render(request, self.template_name, {'order': order})


# ---------------- SOTUVCHI KO'RINISHI (VENDOR) ---------------- #

class SellerOrderListView(LoginRequiredMixin, View):
    """Sotuvchi o'z do'konlariga tushgan tovarlar ro'yxatini ko'rishi"""
    template_name = 'orders/seller_order_list.html'

    def get(self, request):
        # Faqat foydalanuvchining do'konlariga tegishli OrderItem'lar
        order_items = (
            OrderItem.objects.filter(shop__seller=request.user)
            .select_related('order__user', 'variant__product', 'shop', 'order')
            .order_by('-created_at')
        )
        return render(request, self.template_name, {'order_items': order_items})


class SellerOrderStatusUpdateView(LoginRequiredMixin, View):
    """Sotuvchi buyurtma holatini yangilashi (masalan: Jarayonda -> Yo'lda)"""
    template_name = 'orders/seller_order_status.html'

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk, items__shop__seller=request.user)
        form = OrderStatusUpdateForm(instance=order)
        return render(request, self.template_name, {'form': form, 'order': order})

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk, items__shop__seller=request.user)
        form = OrderStatusUpdateForm(request.POST, instance=order)
        if form.is_valid():
            updated_order = form.save()
            
            # YAngi qatorlar: Agar buyurtma bekor qilingan bo'lsa, omborga qaytarish
            if updated_order.status == Order.StatusChoices.CANCELLED:
                for item in updated_order.items.all():
                    item.variant.stock = F('stock') + item.quantity
                    item.variant.save(update_fields=['stock'])
                    
            messages.success(request, f"#{order.id} buyurtma holati yangilandi.")
            return redirect('orders:seller_orders')
        return render(request, self.template_name, {'form': form, 'order': order})