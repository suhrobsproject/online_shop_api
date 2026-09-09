from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import Shop
from .forms import ShopCreateForm, ShopUpdateForm


class ShopCreateView(LoginRequiredMixin, View):
    template_name = 'shops/shop_form.html'

    def get(self, request):
        form = ShopCreateForm()
        return render(request, self.template_name, {'form': form, 'title': "Yangi do‘kon ochish"})

    def post(self, request):
        form = ShopCreateForm(request.POST, request.FILES)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.seller = request.user
            shop.save()

            # Agar foydalanuvchi roli hali 'seller' bo'lmasa, yangilaymiz
            if request.user.role != 'seller':
                request.user.role = 'seller'
                request.user.save(update_fields=['role'])

            messages.success(request, f"'{shop.name}' do‘koni ochildi va tekshiruvga yuborildi.")
            return redirect('shops:my_shops')

        return render(request, self.template_name, {'form': form, 'title': "Yangi do‘kon ochish"})


class ShopUpdateView(LoginRequiredMixin, View):
    template_name = 'shops/shop_form.html'

    def get(self, request, slug):
        # Faqat o'ziga tegishli do'konni tahrirlash imkoniyati
        shop = get_object_or_404(Shop, slug=slug, seller=request.user)
        form = ShopUpdateForm(instance=shop)
        return render(request, self.template_name, {'form': form, 'shop': shop, 'title': "Do‘konni tahrirlash"})

    def post(self, request, slug):
        shop = get_object_or_404(Shop, slug=slug, seller=request.user)
        form = ShopUpdateForm(request.POST, request.FILES, instance=shop)
        if form.is_valid():
            updated_shop = form.save()
            messages.success(request, "Do‘kon ma’lumotlari muvaffaqiyatli yangilandi.")
            return redirect('shops:detail', slug=updated_shop.slug)

        return render(request, self.template_name, {'form': form, 'shop': shop, 'title': "Do‘konni tahrirlash"})


class ShopDetailView(View):
    template_name = 'shops/shop_detail.html'

    def get(self, request, slug):
        # Do'kon barcha xaridorlarga ko'rinadi (slug bo'yicha qidiriladi)
        shop = get_object_or_404(Shop, slug=slug)
        return render(request, self.template_name, {'shop': shop})


class MyShopsListView(LoginRequiredMixin, View):
    template_name = 'shops/my_shops.html'

    def get(self, request):
        # Foydalanuvchining faqat o'ziga tegishli do'konlari
        shops = Shop.objects.filter(seller=request.user)
        return render(request, self.template_name, {'shops': shops})


class ShopDeleteView(LoginRequiredMixin, View):
    def post(self, request, slug):
        shop = get_object_or_404(Shop, slug=slug, seller=request.user)
        shop_name = shop.name
        shop.delete()

        # Agar sotuvchining boshqa do'koni qolmagan bo'lsa, rolini yana 'customer'ga qaytaramiz
        if not request.user.shops.exists():
            request.user.role = 'customer'
            request.user.save(update_fields=['role'])

        messages.info(request, f"'{shop_name}' do‘koni muvaffaqiyatli o‘chirildi.")
        return redirect('shops:my_shops')