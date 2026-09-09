from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import Comment
from .forms import CommentForm
from products.models import Product
from orders.models import OrderItem


class AddCommentView(LoginRequiredMixin, View):
    """Mahsulot sahifasidan kelgan yangi sharhni saqlash"""
    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)

        # Xaridor bu mahsulotga oldin sharh qoldirganligini tekshirish
        if Comment.objects.filter(user=request.user, product=product).exists():
            messages.warning(request, "Siz ushbu mahsulotga allaqachon sharh qoldirgansiz.")
            return redirect('products:product_detail', slug=product.slug)

        # Xaridor haqiqatdan ham ushbu mahsulotni sotib olganini tekshirish
        has_purchased = OrderItem.objects.filter(
            order__user=request.user,
            order__status='delivered',
            variant__product=product
        ).exists()

        if not has_purchased:
            messages.error(request, "Sharh qoldirish uchun mahsulotni avval sotib olgan bo‘lishingiz kerak.")
            return redirect('products:product_detail', slug=product.slug)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = product
            comment.save()
            messages.success(request, "Sharhingiz qabul qilindi!")
        else:
            messages.error(request, "Sharhni saqlashda xatolik yuz berdi.")

        return redirect('products:product_detail', slug=product.slug)


class DeleteCommentView(LoginRequiredMixin, View):
    """Foydalanuvchi o'zi qoldirgan sharhni o'chirishi"""
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, user=request.user)
        product_slug = comment.product.slug
        comment.delete()
        messages.info(request, "Sharhingiz o‘chirildi.")
        return redirect('products:product_detail', slug=product_slug)