import os, random, urllib.request
from django.utils.text import slugify
from django.db import transaction
from django.core.files import File
from users.models import CustomUser
from shops.models import Shop
from products.models import Category, Product, ProductVariant, ProductImage

def run():
    print("Avvalgi xunuk ma'lumotlar tozalanmoqda...")
    Product.objects.all().delete()
    Category.objects.all().delete()
    
    print("Yangi rasmli va sifatli ma'lumotlar qo'shilmoqda (biroz kuting)...")
    user = CustomUser.objects.filter(is_superuser=True).first()
    shop, _ = Shop.objects.get_or_create(slug="mega-shop", defaults={"name": "Asosiy Do'kon", "seller": user, "is_verified": True})

    data = {
        "Texnika": {
            "Telefonlar": ["iPhone 15 Pro Max", "Samsung Galaxy S24 Ultra", "Xiaomi 14 Pro", "OnePlus 12", "Google Pixel 8 Pro", "Redmi Note 13", "Poco X6 Pro", "Honor Magic 6", "Vivo X100 Pro", "Oppo Find X7"],
            "Kompyuterlar": ["MacBook Pro M3", "Asus ROG Zephyrus", "Dell XPS 15", "Lenovo ThinkPad X1", "HP Spectre x360", "Acer Predator Helios", "MSI Stealth 16", "Razer Blade 15", "LG Gram 17", "Asus Zenbook 14"]
        },
        "Kiyimlar": {
            "Erkaklar kiyimi": ["Qishki Kurtka", "Jinsi shim", "Klassik Ko'ylak", "Sport Kostyum", "Krossovka Nike", "Futbolka Polo", "Qora Palto", "Sviter", "Qishki Etik", "Shlyapa"],
            "Ayollar kiyimi": ["Oqshom Ko'ylagi", "Yozgi Sarafan", "Jinsi Pidjak", "Kardigan", "Oyoq kiyim (Tuflik)", "Sharvovar shim", "Qishki Palto", "Sport formasi", "Sumka Gucci", "Quyosh ko'zoynagi"]
        },
        "Uy anjomlari": {
            "Oshxona anjomlari": ["Blender Philips", "Mikroto'lqinli pech Samsung", "Gaz plita Artel", "Toster Bosch", "Qahva qaynatgich Delonghi", "Choynak Tefal", "Muzlatgich LG", "Idish yuvish mashinasi Beko", "Go'sht qiymalagich", "Oshxona tarozisi"]
        }
    }

    media_dir = "media/products/images"
    os.makedirs(media_dir, exist_ok=True)

    with transaction.atomic():
        for parent_title, subcats in data.items():
            parent_cat, _ = Category.objects.get_or_create(title=parent_title)
            for child_title, products in subcats.items():
                child_cat, _ = Category.objects.get_or_create(title=child_title, parent=parent_cat)
                for prod_title in products:
                    slug = slugify(prod_title) + f"-{random.randint(100, 999)}"
                    product = Product.objects.create(shop=shop, category=child_cat, title=prod_title, slug=slug, description=f"{prod_title} eng yaxshi sifat bilan.")
                    price = random.randint(100, 1500)
                    has_discount = random.choice([True, False])
                    old_price = price + random.randint(50, 300) if has_discount else None
                    ProductVariant.objects.create(product=product, price=price, old_price=old_price, stock=random.randint(5, 50), attributes={"Brend": prod_title.split()[0]})
                    
                    try:
                        img_path = os.path.join(media_dir, f"{slug}.jpg")
                        urllib.request.urlretrieve(f"https://picsum.photos/seed/{slug}/400/400", img_path)
                        with open(img_path, 'rb') as f:
                            ProductImage.objects.create(product=product, image=File(f, name=f"{slug}.jpg"), is_main=True)
                    except:
                        pass
    print("Barcha ma'lumotlar va rasmlar muvaffaqiyatli yuklandi! 🎉")
run()
