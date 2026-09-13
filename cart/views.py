from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages

from .models import Cart, CartItem
from products.models import ProductVariant
from .forms import AddToCartForm, UpdateCartItemForm


def _get_or_create_cart(request):
    """
    Foydalanuvchi tizimga kirgan bo'lsa user bo'yicha,
    kirmagan bo'lsa session_key bo'yicha savatni topadi yoki yangisini ochadi.
    """
    if not request.session.session_key:
        request.session.create()

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)

    return cart


class CartDetailView(View):
    template_name = 'cart/cart_detail.html'

    def get(self, request):
        cart = _get_or_create_cart(request)
        cart_items = (
            cart.items.select_related('variant__product', 'variant__product__shop')
            .prefetch_related('variant__images')
        )

        return render(request, self.template_name, {
            'cart': cart,
            'cart_items': cart_items
        })


class AddToCartView(View):
    def post(self, request, variant_id):
        variant = get_object_or_404(ProductVariant, pk=variant_id)
        form = AddToCartForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart = _get_or_create_cart(request)

            # Ombordagi qoldiqni tekshirish
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                variant=variant,
                defaults={'quantity': quantity}
            )

            if not created:
                if cart_item.quantity + quantity > variant.stock:
                    messages.error(request, f"Omborda faqat {variant.stock} dona mavjud.")
                    return redirect('cart:cart_detail')
                cart_item.quantity += quantity
                cart_item.save(update_fields=['quantity'])
            else:
                if quantity > variant.stock:
                    messages.error(request, f"Omborda faqat {variant.stock} dona mavjud.")
                    cart_item.delete()
                    return redirect('cart:cart_detail')

            messages.success(request, f"'{variant.product.title}' savatga qo‘shildi.")

        return redirect('cart:cart_detail')


class UpdateCartItemView(View):
    def post(self, request, item_id):
        cart = _get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, pk=item_id, cart=cart)
        form = UpdateCartItemForm(request.POST)

        if form.is_valid():
            new_quantity = form.cleaned_data['quantity']
            if new_quantity > cart_item.variant.stock:
                messages.error(request, f"Omborda faqat {cart_item.variant.stock} dona mavjud.")
            else:
                cart_item.quantity = new_quantity
                cart_item.save(update_fields=['quantity'])
                messages.success(request, "Miqdor yangilandi.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

        return redirect('cart:cart_detail')


class RemoveFromCartView(View):
    def post(self, request, item_id):
        cart = _get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, pk=item_id, cart=cart)
        cart_item.delete()
        messages.info(request, "Mahsulot savatdan olib tashlandi.")
        return redirect('cart:cart_detail')