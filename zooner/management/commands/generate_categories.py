from django.core.management.base import BaseCommand
from zooner.models import Category
from django.utils.text import slugify
import uuid

class Command(BaseCommand):
    help = 'Generate sample business categories'

    def handle(self, *args, **kwargs):
        categories = [
            {"name": "Restaurants", "description": "Places offering food and drink", "icon": "🍽️", "color": "#ff5733"},
            {"name": "Shops", "description": "Retail stores and outlets", "icon": "🛍️", "color": "#33c1ff"},
            {"name": "Barbershops", "description": "Haircuts and grooming services", "icon": "💈", "color": "#d63384"},
            {"name": "Hotels", "description": "Accommodation and lodging", "icon": "🏨", "color": "#6f42c1"},
            {"name": "Supermarkets", "description": "General groceries and essentials", "icon": "🛒", "color": "#20c997"},
            {"name": "Pharmacies", "description": "Medical and health-related products", "icon": "💊", "color": "#6610f2"},
            {"name": "Salons", "description": "Beauty and hair care services", "icon": "💇‍♀️", "color": "#e83e8c"},
            {"name": "Electronics", "description": "Electronic gadgets and appliances", "icon": "🔌", "color": "#17a2b8"},
            {"name": "Tailors", "description": "Custom clothing and repair", "icon": "🧵", "color": "#fd7e14"},
            {"name": "Transport", "description": "Transport and logistics services", "icon": "🚗", "color": "#28a745"},
            {"name": "Education", "description": "Learning and academic services", "icon": "📚", "color": "#ffc107"},
            {"name": "Repairs", "description": "Appliance and general repairs", "icon": "🔧", "color": "#6c757d"},
            {"name": "Fitness", "description": "Gyms and personal training", "icon": "🏋️", "color": "#dc3545"},
            {"name": "Bakeries", "description": "Bread, cakes, and pastries", "icon": "🍞", "color": "#795548"},
            {"name": "Butcheries", "description": "Fresh meat and related services", "icon": "🥩", "color": "#c0392b"},
            {"name": "Car Wash", "description": "Vehicle cleaning and polishing", "icon": "🚿", "color": "#5bc0de"},
            {"name": "Photography", "description": "Photo and video services", "icon": "📸", "color": "#8e44ad"},
            {"name": "Printing", "description": "Document and banner printing", "icon": "🖨️", "color": "#3c8dbc"},
            {"name": "Internet Cafes", "description": "Computer access and printing", "icon": "💻", "color": "#00b894"},
            {"name": "Cleaning Services", "description": "Home and office cleaning", "icon": "🧹", "color": "#27ae60"},
        ]

        created, skipped = 0, 0

        for i, cat in enumerate(categories):
            slug = slugify(cat["name"])
            obj, created_flag = Category.objects.get_or_create(
                name=cat["name"],
                defaults={
                    "slug": slug,
                    "description": cat["description"],
                    "icon": cat["icon"],
                    "color": cat["color"],
                    "is_active": True,
                    "order": i + 1
                }
            )
            if created_flag:
                created += 1
            else:
                skipped += 1

        self.stdout.write(self.style.SUCCESS(f"✅ {created} categories created, {skipped} already existed."))
