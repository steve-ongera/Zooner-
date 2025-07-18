# Generated by Django 5.2 on 2025-07-01 14:10

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True)),
                ('icon', models.CharField(blank=True, max_length=50)),
                ('color', models.CharField(default='#007bff', max_length=7)),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Town',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('country', models.CharField(default='Kenya', max_length=100)),
                ('region', models.CharField(blank=True, max_length=100)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('role', models.CharField(choices=[('user', 'General User'), ('business', 'Business Owner'), ('admin', 'Administrator')], default='user', max_length=10)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_images/')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('is_verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('last_active', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(max_length=1000)),
                ('address', models.TextField(blank=True, max_length=500)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('phone', models.CharField(blank=True, max_length=15)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('website', models.URLField(blank=True)),
                ('hero_image', models.ImageField(blank=True, null=True, upload_to='business_images/')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='business_logos/')),
                ('business_hours', models.JSONField(blank=True, default=dict)),
                ('status', models.CharField(choices=[('pending', 'Pending Approval'), ('active', 'Active'), ('suspended', 'Suspended'), ('closed', 'Closed')], default='pending', max_length=10)),
                ('is_featured', models.BooleanField(default=False)),
                ('is_verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_businesses', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='businesses', to='zooner.category')),
                ('town', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='businesses', to='zooner.town')),
            ],
            options={
                'verbose_name_plural': 'Businesses',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('chat_type', models.CharField(choices=[('user_business', 'User to Business'), ('user_user', 'User to User')], default='user_business', max_length=15)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('business', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chats', to='zooner.business')),
                ('participants', models.ManyToManyField(related_name='chats', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.TextField(blank=True, max_length=1000)),
                ('message_type', models.CharField(choices=[('text', 'Text Message'), ('image', 'Image'), ('file', 'File'), ('system', 'System Message')], default='text', max_length=10)),
                ('attachment', models.FileField(blank=True, null=True, upload_to='chat_attachments/')),
                ('is_read', models.BooleanField(default=False)),
                ('read_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='zooner.chat')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('caption', models.TextField(max_length=2000)),
                ('post_type', models.CharField(choices=[('update', 'General Update'), ('promotion', 'Promotion/Offer'), ('event', 'Event'), ('product', 'Product Showcase'), ('announcement', 'Announcement')], default='update', max_length=15)),
                ('image', models.ImageField(blank=True, null=True, upload_to='post_images/')),
                ('video', models.FileField(blank=True, null=True, upload_to='post_videos/')),
                ('tags', models.JSONField(blank=True, default=list)),
                ('likes_count', models.PositiveIntegerField(default=0)),
                ('comments_count', models.PositiveIntegerField(default=0)),
                ('shares_count', models.PositiveIntegerField(default=0)),
                ('views_count', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('is_pinned', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('published_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authored_posts', to=settings.AUTH_USER_MODEL)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='zooner.business')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='zooner.category')),
            ],
            options={
                'ordering': ['-published_at'],
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('notification_type', models.CharField(choices=[('like', 'Post Liked'), ('comment', 'Post Commented'), ('follow', 'New Follower'), ('message', 'New Message'), ('post', 'New Post from Followed Business'), ('system', 'System Notification'), ('promotion', 'Promotional Notification')], max_length=15)),
                ('title', models.CharField(max_length=200)),
                ('message', models.TextField(max_length=500)),
                ('is_read', models.BooleanField(default=False)),
                ('is_sent', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('read_at', models.DateTimeField(blank=True, null=True)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
                ('related_business', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='zooner.business')),
                ('related_chat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='zooner.chat')),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent_notifications', to=settings.AUTH_USER_MODEL)),
                ('related_post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='zooner.post')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.TextField(max_length=500)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='zooner.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='zooner.post')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='ReportedContent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('report_type', models.CharField(choices=[('spam', 'Spam'), ('inappropriate', 'Inappropriate Content'), ('harassment', 'Harassment'), ('fake', 'Fake Business/Profile'), ('copyright', 'Copyright Violation'), ('other', 'Other')], max_length=15)),
                ('reason', models.TextField(max_length=500)),
                ('status', models.CharField(choices=[('pending', 'Pending Review'), ('reviewed', 'Reviewed'), ('resolved', 'Resolved'), ('dismissed', 'Dismissed')], default='pending', max_length=10)),
                ('admin_notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('reviewed_at', models.DateTimeField(blank=True, null=True)),
                ('reported_business', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='zooner.business')),
                ('reported_post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='zooner.post')),
                ('reported_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reports_against', to=settings.AUTH_USER_MODEL)),
                ('reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports_made', to=settings.AUTH_USER_MODEL)),
                ('reviewed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewed_reports', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='UserEngagement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('engagement_type', models.CharField(choices=[('view', 'Post View'), ('profile_view', 'Business Profile View'), ('search', 'Search Query'), ('app_open', 'App Opened'), ('session_duration', 'Session Duration')], max_length=20)),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('session_id', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('related_business', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='zooner.business')),
                ('related_post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='zooner.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='engagements', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='BusinessAnalytics',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('profile_views', models.PositiveIntegerField(default=0)),
                ('post_views', models.PositiveIntegerField(default=0)),
                ('new_followers', models.PositiveIntegerField(default=0)),
                ('total_likes', models.PositiveIntegerField(default=0)),
                ('total_comments', models.PositiveIntegerField(default=0)),
                ('total_shares', models.PositiveIntegerField(default=0)),
                ('engagement_rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('reach', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='analytics', to='zooner.business')),
            ],
            options={
                'ordering': ['-date'],
                'unique_together': {('business', 'date')},
            },
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='zooner.business')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'business')},
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='zooner.post')),
            ],
            options={
                'unique_together': {('user', 'post')},
            },
        ),
    ]
