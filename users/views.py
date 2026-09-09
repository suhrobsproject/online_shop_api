from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import CustomUser, Address
from .forms import (
    CustomUserRegisterForm,
    CustomUserLoginForm,
    CustomUserProfileForm,
    CustomUserChangePasswordForm,
    UserProfileUpdateForm,
    AddressForm
)


class RegisterView(View):
    template_name = 'users/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = CustomUserRegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = CustomUserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Ro'yxatdan muvaffaqiyatli o'tdingiz!")
            return redirect('home')
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    template_name = 'users/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = CustomUserLoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.phone_number}!")
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "Tizimdan muvaffaqiyatli chiqdingiz.")
        return redirect('login')


class ProfileView(LoginRequiredMixin, View):
    template_name = 'users/profile.html'

    def get(self, request):
        form = CustomUserProfileForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomUserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil ma'lumotlaringiz yangilandi!")
            return redirect('profile')
        return render(request, self.template_name, {'form': form})



class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = 'users/profile_update.html'

    def get(self, request):
        # Formani foydalanuvchining joriy ma'lumotlari bilan to'ldirib ko'rsatamiz
        form = UserProfileUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # Kiritilgan yangi ma'lumotlarni qabul qilamiz
        form = UserProfileUpdateForm(request.POST, instance=request.user)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Profil ma'lumotlaringiz muvaffaqiyatli yangilandi!")
            # Tahrirlab bo'lgach, asosiy profil sahifasiga qaytarib yuboramiz
            return redirect('users:profile')
        
        # Agar xatolik bo'lsa (masalan email band bo'lsa), formani xatolari bilan birga qaytaramiz
        return render(request, self.template_name, {'form': form})

class ChangePasswordView(LoginRequiredMixin, View):
    template_name = 'users/change_password.html'

    def get(self, request):
        form = CustomUserChangePasswordForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomUserChangePasswordForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            # Parol almashganda foydalanuvchini sessiyadan chiqarib yubormaslik uchun
            update_session_auth_hash(request, user)
            messages.success(request, "Parolingiz muvaffaqiyatli o'zgartirildi!")
            return redirect('profile')
        return render(request, self.template_name, {'form': form})


class AddressListView(LoginRequiredMixin, View):
    template_name = 'users/address_list.html'

    def get(self, request):
        addresses = Address.objects.filter(user=request.user)
        form = AddressForm()
        return render(request, self.template_name, {
            'addresses': addresses,
            'form': form
        })

    def post(self, request):
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, "Yangi manzil muvaffaqiyatli qo'shildi.")
            return redirect('address_list')
        
        addresses = Address.objects.filter(user=request.user)
        return render(request, self.template_name, {
            'addresses': addresses,
            'form': form
        })


class AddressUpdateView(LoginRequiredMixin, View):
    template_name = 'users/address_form.html'

    def get(self, request, pk):
        address = get_object_or_404(Address, pk=pk, user=request.user)
        form = AddressForm(instance=address)
        return render(request, self.template_name, {'form': form, 'address': address})

    def post(self, request, pk):
        address = get_object_or_404(Address, pk=pk, user=request.user)
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, "Manzil yangilandi.")
            return redirect('address_list')
        return render(request, self.template_name, {'form': form, 'address': address})


class AddressDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        address = get_object_or_404(Address, pk=pk, user=request.user)
        address.delete()
        messages.success(request, "Manzil o'chirildi.")
        return redirect('address_list')