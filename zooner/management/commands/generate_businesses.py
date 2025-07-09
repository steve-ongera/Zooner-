from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from zooner.models import Business, Town, Category
from django.utils.text import slugify
from random import choice, randint, uniform
import faker
import uuid

fake = faker.Faker()
User = get_user_model()

class Command(BaseCommand):
    help = 'Generate sample businesses for testing'

    def handle(self, *args, **kwargs):
        owners = User.objects.all()
        towns = Town.objects.all()
        categories = Category.objects.all()

        if not owners.exists():
            self.stdout.write(self.style.ERROR("❌ No users found. Please create at least one user."))
            return

        if not towns.exists():
            self.stdout.write(self.style.ERROR("❌ No towns found. Please run `generate_towns` first."))
            return

        if not categories.exists():
            self.stdout.write(self.style.ERROR("❌ No categories found. Please run `generate_categories` first."))
            return

        business_names = [
            "Jumbo Mart", "Tech Savvy", "Fresh Bites", "Bella Salon", "Quick Cleaners",
            "Smart Electronics", "Sunrise Pharmacy", "Urban Gym", "Blue Bakery", "Classic Tailors",
            "Happy Kids School", "Green Gardens", "Safari Rides", "Sparkle Auto", "Digital Hub",
            "Mama Mboga", "Tamu Treats", "Photo Point", "Prime Print", "The Wellness Spot"
        ]

        created = 0

        for name in business_names:
            owner = choice(owners)
            town = choice(towns)
            category = choice(categories)
            slug = slugify(name) + "-" + uuid.uuid4().hex[:5]

            description = fake.text(max_nb_chars=300)
            email = fake.email()
            phone = fake.phone_number()
            address = fake.address()
            lat = round(uniform(-1.5, 1.5), 6)
            lon = round(uniform(34.0, 40.0), 6)
            website = fake.url()
            hours = {
                "Monday": "8am - 6pm",
                "Tuesday": "8am - 6pm",
                "Wednesday": "8am - 6pm",
                "Thursday": "8am - 6pm",
                "Friday": "8am - 6pm",
                "Saturday": "9am - 4pm",
                "Sunday": "Closed"
            }

            Business.objects.create(
                owner=owner,
                name=name,
                slug=slug,
                description=description,
                town=town,
                address=address,
                latitude=lat,
                longitude=lon,
                category=category,
                phone=phone,
                email=email,
                website=website,
                business_hours=hours,
                status=choice(['active', 'pending', 'suspended']),
                is_featured=choice([True, False]),
                is_verified=choice([True, False])
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f"✅ {created} businesses created successfully."))
