import random
from django.utils.text import slugify
from django.db import transaction
from users.models import CustomUser
from shops.models import Shop
from products.models import Category, Product, ProductVariant

def run():
    print("Seeding data boshlandi...")

    user, created = CustomUser.objects.get_or_create(
        phone_number="+998901234567",
        defaults={"role": "seller", "first_name": "Test", "is_staff": True, "is_superuser": True}
    )
    if created:
        user.set_password("admin123")
        user.save()

    # Xatolikni oldini olish uchun slug bo'yicha qidiramiz
    shop1, _ = Shop.objects.get_or_create(
        slug="auto-shop-1", 
        defaults={"name": "Avto Do'kon 1", "seller": user, "is_verified": True}
    )
    shop2, _ = Shop.objects.get_or_create(
        slug="auto-shop-2", 
        defaults={"name": "Avto Do'kon 2", "seller": user, "is_verified": True}
    )

    categories_data = {
        "Elektronika": ["Smartfonlar", "Noutbuklar", "Televizorlar"],
        "Kiyim-kechak": ["Erkaklar kiyimi", "Ayollar kiyimi", "Bolalar kiyimi"],
        "Uy anjomlari": ["Oshxona anjomlari", "Mebellar"],
    }

    with transaction.atomic():
        for parent_title, children in categories_data.items():
            parent_cat, _ = Category.objects.get_or_create(title=parent_title)
            
            for child_title in children:
                child_cat, _ = Category.objects.get_or_create(title=child_title, parent=parent_cat)
                shop = shop1 if parent_title == "Elektronika" else shop2
                
                for i in range(1, 11):
                    prod_title = f"{child_title} - Model {i}"
                    base_slug = slugify(prod_title)
                    unique_slug = f"{base_slug}-{random.randint(1000, 9999)}"
                    
                    product, p_created = Product.objects.get_or_create(
                        shop=shop,
                        category=child_cat,
                        title=prod_title,
                        defaults={
                            "slug": unique_slug,
                            "description": f"Bu ajoyib {prod_title}. Juda sifatli va hamyonbop!"
                        }
                    )
                    
                    if p_created:
                        price = random.randint(100, 1500)
                        has_discount = random.choice([True, False])
                        old_price = price + random.randint(50, 300) if has_discount else None
                        
                        ProductVariant.objects.create(
                            product=product,
                            price=price,
                            old_price=old_price,
                            stock=random.randint(10, 100),
                            attributes={"Kafolat": "1 yil"}
                        )
                
        print("Barcha toifalar va mahsulotlar muvaffaqiyatli qo'shildi! 🎉")

run()
