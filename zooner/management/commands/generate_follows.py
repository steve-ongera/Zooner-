from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from zooner.models import Follow, Business
from random import choice, sample
import uuid

User = get_user_model()

class Command(BaseCommand):
    help = 'Generate user-business follow relationships'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        businesses = Business.objects.all()

        if not users.exists():
            self.stdout.write(self.style.ERROR("❌ No users found."))
            return

        if not businesses.exists():
            self.stdout.write(self.style.ERROR("❌ No businesses found."))
            return

        created = 0
        skipped = 0

        for user in users:
            # Each user follows 3–7 random businesses
            followed_businesses = sample(list(businesses), min(len(businesses), choice([3, 4, 5, 6, 7])))

            for biz in followed_businesses:
                # Avoid duplicate follows
                if Follow.objects.filter(user=user, business=biz).exists():
                    skipped += 1
                    continue

                Follow.objects.create(user=user, business=biz)
                created += 1

        self.stdout.write(self.style.SUCCESS(f"✅ {created} follows created, {skipped} skipped (already existed)."))
