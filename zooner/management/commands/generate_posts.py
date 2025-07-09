from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from zooner.models import Post, Business, Category
from random import choice, randint, sample
import faker

fake = faker.Faker()
User = get_user_model()

class Command(BaseCommand):
    help = 'Generate sample business posts'

    def handle(self, *args, **kwargs):
        businesses = Business.objects.all()
        users = User.objects.all()
        categories = Category.objects.all()

        if not businesses.exists():
            self.stdout.write(self.style.ERROR("❌ No businesses found. Run `generate_businesses` first."))
            return

        if not users.exists():
            self.stdout.write(self.style.ERROR("❌ No users found. Create at least one user."))
            return

        post_types = ['update', 'promotion', 'event', 'product', 'announcement']
        hashtags_pool = ['#offer', '#new', '#event', '#discount', '#update', '#launch', '#special', '#business', '#local', '#shop']

        created = 0

        for business in businesses:
            for _ in range(randint(2, 5)):  # Generate 2 to 5 posts per business
                caption = fake.sentence(nb_words=15)
                post_type = choice(post_types)
                tags = sample(hashtags_pool, randint(2, 5))
                author = business.owner
                category = choice(categories)

                Post.objects.create(
                    business=business,
                    author=author,
                    caption=caption,
                    post_type=post_type,
                    tags=tags,
                    category=category,
                    likes_count=randint(0, 100),
                    comments_count=randint(0, 50),
                    shares_count=randint(0, 30),
                    views_count=randint(10, 500),
                    is_active=True,
                    is_featured=choice([True, False]),
                    is_pinned=choice([True, False]),
                    published_at=timezone.now()
                )
                created += 1

        self.stdout.write(self.style.SUCCESS(f"✅ {created} posts generated successfully."))
