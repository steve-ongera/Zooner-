from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from zooner.models import Like, Post
from random import sample, randint

User = get_user_model()

class Command(BaseCommand):
    help = 'Generate random likes for posts'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        posts = Post.objects.all()

        if not users.exists():
            self.stdout.write(self.style.ERROR("❌ No users found. Please create users first."))
            return

        if not posts.exists():
            self.stdout.write(self.style.ERROR("❌ No posts found. Please generate posts first."))
            return

        created = 0
        skipped = 0

        for user in users:
            # Randomly like 5–10 posts per user
            liked_posts = sample(list(posts), min(len(posts), randint(5, 10)))

            for post in liked_posts:
                if Like.objects.filter(user=user, post=post).exists():
                    skipped += 1
                    continue

                Like.objects.create(user=user, post=post)
                created += 1

        self.stdout.write(self.style.SUCCESS(f"✅ {created} likes created, {skipped} skipped (already existed)."))
