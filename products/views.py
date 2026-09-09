from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from .models import Category, Product, ProductVariant, ProductImage
from .forms import ProductForm, ProductVariantFormSet, ProductImageFormSet




class CategoryListView(View):
    """
    Bosh sahifa yoki alohida sahifada barcha bosh kategoriyalar 
    va ularning ichki bo'limlarini (daraxtsimon menyu) ko'rsatish
    """
    template_name = 'products/category_list.html'

    def get(self, request):
        # parent=None orqali faqat asosiy toifalarni olamiz
        # prefetch_related('children') orqali 1 ta so'rovda barcha subkategoriyalar birga tortiladi
        main_categories = Category.objects.filter(parent=None).prefetch_related('children')
        
        return render(request, self.template_name, {
            'categories': main_categories
        })


class CategoryProductsView(View):
    """
    Xaridor ma'lum bir toifani tanlaganda (slug bo'yicha),
    shu toifa va uning barcha ichki toifalariga tegishli mahsulotlarni chiqarish
    """
    template_name = 'products/category_products.html'

    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug)

        # Joriy toifa va uning bevosita bolalari ID larini yig'amiz
        category_ids = [category.id] + list(category.children.values_list('id', flat=True))

        # Shu kategoriyadagi faol do'konlar tovarlarini olish
        products = (
            Product.objects.filter(category_id__in=category_ids, shop__is_verified=True)
            .select_related('shop', 'category')
            .prefetch_related('images', 'variants')
        )

        return render(request, self.template_name, {
            'category': category,
            'products': products
        })
# ---------------- XARIDORLAR UCHUN (PUBLIC) ---------------- #


class ProductListView(View):
    template_name = 'products/product_list.html'

    def get(self, request):
        category_slug = request.GET.get('category')
        
        # Baza optimizatsiyasi: shop, category, asosiy rasm va variantlarni bitta so'rovda tortib olish
        products = Product.objects.filter(shop__is_verified=True).select_related('shop', 'category').prefetch_related('images', 'variants')

        current_category = None
        if category_slug:
            current_category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=current_category)

        categories = Category.objects.filter(parent=None).prefetch_related('children')

        return render(request, self.template_name, {
            'products': products,
            'categories': categories,
            'current_category': current_category
        })



class ProductDetailView(View):
    template_name = 'products/product_detail.html'

    def get(self, request, slug):
        product = get_object_or_404(
            Product.objects.select_related('shop', 'category').prefetch_related('images', 'variants'),
            slug=slug
        )
        return render(request, self.template_name, {'product': product})


# ---------------- SOTUVCHILAR UCHUN CRUD (VENDOR) ---------------- #

class SellerProductListView(LoginRequiredMixin, View):
    template_name = 'products/seller_product_list.html'

    def get(self, request):
        # Faqat joriy foydalanuvchining do'konlariga tegishli mahsulotlar
        products = Product.objects.filter(shop__seller=request.user).select_related('shop', 'category').prefetch_related('variants', 'images')
        return render(request, self.template_name, {'products': products})


class ProductCreateView(LoginRequiredMixin, View):
    template_name = 'products/product_form.html'

    def get(self, request):
        if not request.user.shops.exists():
            messages.warning(request, "Mahsulot qo'shishdan oldin kamida bitta do'kon ochishingiz kerak.")
            return redirect('shops:create')

        form = ProductForm(user=request.user)
        variant_formset = ProductVariantFormSet(prefix='variants')
        image_formset = ProductImageFormSet(prefix='images')

        return render(request, self.template_name, {
            'form': form,
            'variant_formset': variant_formset,
            'image_formset': image_formset,
            'title': "Yangi mahsulot qo'shish"
        })

    def post(self, request):
        form = ProductForm(request.POST, user=request.user)
        variant_formset = ProductVariantFormSet(request.POST, prefix='variants')
        image_formset = ProductImageFormSet(request.POST, request.FILES, prefix='images')

        if form.is_valid() and variant_formset.is_valid() and image_formset.is_valid():
            # Tranzaksiya: mahsulot, uning variantlari yoki rasmlaridan biri saqlanmay qolsa bazani orqaga qaytaradi (Rollback)
            with transaction.atomic():
                product = form.save()
                variant_formset.instance = product
                variant_formset.save()
                image_formset.instance = product
                image_formset.save()

            messages.success(request, f"'{product.title}' muvaffaqiyatli qo'shildi!")
            return redirect('products:seller_products')

        return render(request, self.template_name, {
            'form': form,
            'variant_formset': variant_formset,
            'image_formset': image_formset,
            'title': "Yangi mahsulot qo'shish"
        })


class ProductUpdateView(LoginRequiredMixin, View):
    template_name = 'products/product_form.html'

    def get(self, request, slug):
        # Faqat o'ziga tegishli mahsulotni tahrirlay olishi kerak
        product = get_object_or_404(Product, slug=slug, shop__seller=request.user)
        form = ProductForm(instance=product, user=request.user)
        variant_formset = ProductVariantFormSet(instance=product, prefix='variants')
        image_formset = ProductImageFormSet(instance=product, prefix='images')

        return render(request, self.template_name, {
            'form': form,
            'variant_formset': variant_formset,
            'image_formset': image_formset,
            'product': product,
            'title': "Mahsulotni tahrirlash"
        })

    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug, shop__seller=request.user)
        form = ProductForm(request.POST, instance=product, user=request.user)
        variant_formset = ProductVariantFormSet(request.POST, instance=product, prefix='variants')
        image_formset = ProductImageFormSet(request.POST, request.FILES, instance=product, prefix='images')

        if form.is_valid() and variant_formset.is_valid() and image_formset.is_valid():
            with transaction.atomic():
                product = form.save()
                variant_formset.save()
                image_formset.save()

            messages.success(request, "Mahsulot yangilandi!")
            return redirect('products:seller_products')

        return render(request, self.template_name, {
            'form': form,
            'variant_formset': variant_formset,
            'image_formset': image_formset,
            'product': product,
            'title': "Mahsulotni tahrirlash"
        })


class ProductDeleteView(LoginRequiredMixin, View):
    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug, shop__seller=request.user)
        title = product.title
        product.delete()
        messages.info(request, f"'{title}' mahsuloti o'chirildi.")
        return redirect('products:seller_products')