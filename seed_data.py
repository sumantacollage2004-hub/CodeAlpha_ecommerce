from django.core.management.base import BaseCommand
from store.models import Category, Product

class Command(BaseCommand):
    help = 'Seed initial product & category data (INR prices)'

    def handle(self, *args, **kwargs):
        cats = {
            'electronics': Category.objects.get_or_create(name='Electronics', slug='electronics', icon='fa-laptop')[0],
            'fashion': Category.objects.get_or_create(name='Fashion', slug='fashion', icon='fa-tshirt')[0],
            'home': Category.objects.get_or_create(name='Home & Living', slug='home', icon='fa-home')[0],
            'beauty': Category.objects.get_or_create(name='Beauty', slug='beauty', icon='fa-spa')[0],
        }

        products = [
            dict(name='Sony WH-1000XM5 Headphones', category=cats['electronics'], price=24990, original_price=34990, rating=4.8, review_count=2341, stock=15, badge='hot', image_url='https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500', description='Industry-leading noise cancellation headphones.', features=['ANC Technology','30hr Battery','Touch Controls']),
            dict(name='Apple iPhone 15 Pro', category=cats['electronics'], price=129900, original_price=134900, rating=4.9, review_count=8762, stock=8, badge='new', image_url='https://images.unsplash.com/photo-1695048133142-1a20484429be?w=500', description='Titanium design with A17 Pro chip.', features=['A17 Pro Chip','48MP Camera','5x Optical Zoom']),
            dict(name='Silk Embroidered Kurta Set', category=cats['fashion'], price=3499, original_price=5999, rating=4.6, review_count=892, stock=23, badge='sale', image_url='https://images.unsplash.com/photo-1583391733956-6c78276477e2?w=500', description='Premium silk kurta with intricate handcrafted embroidery.', features=['Pure Silk','Hand Embroidery','Festive Wear']),
            dict(name='Aromatherapy Diffuser Set', category=cats['beauty'], price=1899, original_price=2999, rating=4.5, review_count=567, stock=34, badge=None, image_url='https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=500', description='Ultrasonic cool mist diffuser with 10 premium essential oils.', features=['10 Essential Oils','500ml Tank','Auto Shutoff']),
            dict(name='Handcrafted Teak Wood Bookshelf', category=cats['home'], price=12999, original_price=18999, rating=4.7, review_count=234, stock=6, badge=None, image_url='https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=500', description='5-tier solid teak bookshelf with premium finish.', features=['Solid Teak Wood','5 Tiers','Eco-Certified']),
            dict(name='Samsung 4K QLED Smart TV 55"', category=cats['electronics'], price=74990, original_price=95990, rating=4.7, review_count=3218, stock=12, badge='hot', image_url='https://images.unsplash.com/photo-1593359677879-a4bb92f4588e?w=500', description='Quantum HDR 32x with QLED technology.', features=['4K QLED','Quantum HDR','Gaming Mode']),
        ]

        for p in products:
            badge = p.pop('badge', None) or ''
            Product.objects.get_or_create(name=p['name'], defaults={**p, 'badge': badge, 'is_active': True})

        self.stdout.write(self.style.SUCCESS('✅ Seed data loaded successfully (prices in INR ₹)'))
