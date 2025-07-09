from django.core.management.base import BaseCommand
from zooner.models import Comment, User, Post
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Generate fake comments for existing posts and users'

    def handle(self, *args, **kwargs):
        fake = Faker()

        users = list(User.objects.all())
        posts = list(Post.objects.all())

        if not users or not posts:
            self.stdout.write(self.style.ERROR("❌ No users or posts found. Please create them first."))
            return

        comments_created = 0

        for _ in range(50):  # Generate 50 top-level comments
            user = random.choice(users)
            post = random.choice(posts)
            content = fake.sentence(nb_words=15)

            comment = Comment.objects.create(
                user=user,
                post=post,
                content=content,
                is_active=random.choice([True, True, True, False]),  # Mostly active
            )
            comments_created += 1

            # Randomly generate 0–3 replies to this comment
            for _ in range(random.randint(0, 3)):
                reply_user = random.choice(users)
                reply_content = fake.sentence(nb_words=10)

                Comment.objects.create(
                    user=reply_user,
                    post=post,
                    parent=comment,
                    content=reply_content,
                    is_active=True
                )
                comments_created += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Successfully created {comments_created} comments and replies."))
