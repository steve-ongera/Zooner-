from django.core.management.base import BaseCommand
from zooner.models import User
from faker import Faker
from django.utils import timezone

class Command(BaseCommand):
    help = "Generate 29 fake users with password 'password123'"

    def handle(self, *args, **kwargs):
        fake = Faker()
        password = 'password123'

        for _ in range(29):
            username = fake.user_name()
            email = fake.unique.email()
            phone = fake.phone_number()
            location = fake.city()
            bio = fake.text(max_nb_chars=200)
            role = fake.random_element(elements=['user', 'business', 'admin'])

            user = User(
                username=username,
                email=email,
                phone_number=phone,
                location=location,
                bio=bio,
                role=role,
                is_verified=fake.boolean(chance_of_getting_true=70),
                last_active=timezone.now()
            )
            user.set_password(password)
            user.save()

        self.stdout.write(self.style.SUCCESS('✅ Successfully created 29 fake users'))
