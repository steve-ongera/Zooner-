from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.utils import timezone
import uuid


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    Used to store: User authentication, profile info, role management
    """
    USER_ROLES = [
        ('user', 'General User'),
        ('business', 'Business Owner'),
        ('admin', 'Administrator'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='user')
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_active = models.DateTimeField(default=timezone.now)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return f"{self.username} ({self.email})"


class Town(models.Model):
    """
    Town/City model for location-based filtering
    Used to store: Available towns, location data for businesses and users
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    country = models.CharField(max_length=100, default='Kenya')
    region = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Business category model for classification
    Used to store: Business categories (restaurants, shops, services, etc.)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # Icon class name or emoji
    color = models.CharField(max_length=7, default='#007bff')  # Hex color code
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name


class Business(models.Model):
    """
    Business profile model
    Used to store: Business information, profiles, contact details
    """
    BUSINESS_STATUS = [
        ('pending', 'Pending Approval'),
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('closed', 'Closed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_businesses')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=1000)
    
    # Location info
    town = models.ForeignKey(Town, on_delete=models.CASCADE, related_name='businesses')
    address = models.TextField(max_length=500, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    
    # Business details
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='businesses')
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    
    # Images
    hero_image = models.ImageField(upload_to='business_images/', blank=True, null=True)
    logo = models.ImageField(upload_to='business_logos/', blank=True, null=True)
    
    # Business hours (stored as JSON)
    business_hours = models.JSONField(default=dict, blank=True)
    
    # Status and metrics
    status = models.CharField(max_length=10, choices=BUSINESS_STATUS, default='pending')
    is_featured = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Businesses'
    
    def __str__(self):
        return f"{self.name} - {self.town.name}"
    
    @property
    def followers_count(self):
        return self.followers.count()
    
    @property
    def posts_count(self):
        return self.posts.count()


class Post(models.Model):
    """
    Business posts model (social media-like content)
    Used to store: Business posts, updates, promotions, content
    """
    POST_TYPES = [
        ('update', 'General Update'),
        ('promotion', 'Promotion/Offer'),
        ('event', 'Event'),
        ('product', 'Product Showcase'),
        ('announcement', 'Announcement'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_posts')
    
    # Content
    caption = models.TextField(max_length=2000)
    post_type = models.CharField(max_length=15, choices=POST_TYPES, default='update')
    
    # Media
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    video = models.FileField(upload_to='post_videos/', blank=True, null=True)
    
    # Categorization
    tags = models.JSONField(default=list, blank=True)  # Store hashtags as list
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Engagement metrics
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    shares_count = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-published_at']
    
    def __str__(self):
        return f"{self.business.name} - {self.caption[:50]}..."


class Follow(models.Model):
    """
    User-Business follow relationship
    Used to store: Follow relationships between users and businesses
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'business']
    
    def __str__(self):
        return f"{self.user.username} follows {self.business.name}"


class Like(models.Model):
    """
    Post likes model
    Used to store: User likes on business posts
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'post']
    
    def __str__(self):
        return f"{self.user.username} likes {self.post.business.name}'s post"


class Comment(models.Model):
    """
    Post comments model
    Used to store: User comments on business posts
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    content = models.TextField(max_length=500)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.user.username} commented on {self.post.business.name}'s post"


class Chat(models.Model):
    """
    Chat/Conversation model for 1:1 messaging
    Used to store: Chat conversations between users and businesses
    """
    CHAT_TYPES = [
        ('user_business', 'User to Business'),
        ('user_user', 'User to User'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name='chats')
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True, related_name='chats')
    chat_type = models.CharField(max_length=15, choices=CHAT_TYPES, default='user_business')
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        participant_names = ", ".join([user.username for user in self.participants.all()])
        return f"Chat: {participant_names}"


class Message(models.Model):
    """
    Individual messages within chats
    Used to store: Chat messages, message content, timestamps
    """
    MESSAGE_TYPES = [
        ('text', 'Text Message'),
        ('image', 'Image'),
        ('file', 'File'),
        ('system', 'System Message'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    
    content = models.TextField(max_length=1000, blank=True)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default='text')
    attachment = models.FileField(upload_to='chat_attachments/', blank=True, null=True)
    
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Message from {self.sender.username} in {self.chat}"


class Notification(models.Model):
    """
    User notifications model
    Used to store: Push notifications, activity alerts, system messages
    """
    NOTIFICATION_TYPES = [
        ('like', 'Post Liked'),
        ('comment', 'Post Commented'),
        ('follow', 'New Follower'),
        ('message', 'New Message'),
        ('post', 'New Post from Followed Business'),
        ('system', 'System Notification'),
        ('promotion', 'Promotional Notification'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='sent_notifications')
    
    notification_type = models.CharField(max_length=15, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField(max_length=500)
    
    # Related objects (optional)
    related_post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    related_business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)
    related_chat = models.ForeignKey(Chat, on_delete=models.CASCADE, null=True, blank=True)
    
    # Status
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)  # For push notifications
    
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.title}"


class UserEngagement(models.Model):
    """
    User engagement tracking model
    Used to store: User activity metrics, analytics data
    """
    ENGAGEMENT_TYPES = [
        ('view', 'Post View'),
        ('profile_view', 'Business Profile View'),
        ('search', 'Search Query'),
        ('app_open', 'App Opened'),
        ('session_duration', 'Session Duration'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='engagements')
    engagement_type = models.CharField(max_length=20, choices=ENGAGEMENT_TYPES)
    
    # Related objects (optional)
    related_post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    related_business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)  # Store additional data
    session_id = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.engagement_type}"


class BusinessAnalytics(models.Model):
    """
    Business analytics and metrics model
    Used to store: Business performance data, engagement metrics
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='analytics')
    
    # Daily metrics
    date = models.DateField()
    profile_views = models.PositiveIntegerField(default=0)
    post_views = models.PositiveIntegerField(default=0)
    new_followers = models.PositiveIntegerField(default=0)
    total_likes = models.PositiveIntegerField(default=0)
    total_comments = models.PositiveIntegerField(default=0)
    total_shares = models.PositiveIntegerField(default=0)
    
    # Engagement metrics
    engagement_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    reach = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['business', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.business.name} analytics for {self.date}"


class ReportedContent(models.Model):
    """
    Content reporting model for moderation
    Used to store: User reports on posts, businesses, or users
    """
    REPORT_TYPES = [
        ('spam', 'Spam'),
        ('inappropriate', 'Inappropriate Content'),
        ('harassment', 'Harassment'),
        ('fake', 'Fake Business/Profile'),
        ('copyright', 'Copyright Violation'),
        ('other', 'Other'),
    ]
    
    REPORT_STATUS = [
        ('pending', 'Pending Review'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_made')
    report_type = models.CharField(max_length=15, choices=REPORT_TYPES)
    reason = models.TextField(max_length=500)
    
    # Reported content (one of these will be filled)
    reported_post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    reported_business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='reports_against')
    
    status = models.CharField(max_length=10, choices=REPORT_STATUS, default='pending')
    admin_notes = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_reports')
    
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Report by {self.reporter.username} - {self.report_type}"