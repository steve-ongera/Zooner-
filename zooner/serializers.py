# ============================================================================
# SERIALIZERS.PY - Data serialization for API responses
# ============================================================================

from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import *

# User Serializers
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password_confirm', 'role', 'phone_number')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'profile_image', 'bio', 
                 'location', 'is_verified', 'followers_count', 'following_count',
                 'created_at', 'last_active')
        read_only_fields = ('id', 'created_at', 'is_verified')
    
    def get_followers_count(self, obj):
        return obj.following.count()
    
    def get_following_count(self, obj):
        return Follow.objects.filter(user=obj).count()

# Town & Category Serializers
class TownSerializer(serializers.ModelSerializer):
    businesses_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Town
        fields = ('id', 'name', 'slug', 'country', 'region', 'businesses_count', 'is_active')
    
    def get_businesses_count(self, obj):
        return obj.businesses.filter(status='active').count()

class CategorySerializer(serializers.ModelSerializer):
    businesses_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description', 'icon', 'color', 'businesses_count')
    
    def get_businesses_count(self, obj):
        return obj.businesses.filter(status='active').count()

# Business Serializers
class BusinessSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    town = TownSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    is_following = serializers.SerializerMethodField()
    recent_posts = serializers.SerializerMethodField()
    
    class Meta:
        model = Business
        fields = ('id', 'name', 'slug', 'description', 'owner', 'town', 'category',
                 'address', 'phone', 'email', 'website', 'hero_image', 'logo',
                 'business_hours', 'status', 'is_featured', 'is_verified',
                 'followers_count', 'posts_count', 'is_following', 'recent_posts',
                 'created_at', 'updated_at')
        read_only_fields = ('id', 'slug', 'followers_count', 'posts_count', 'created_at')
    
    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Follow.objects.filter(user=request.user, business=obj).exists()
        return False
    
    def get_recent_posts(self, obj):
        recent_posts = obj.posts.filter(is_active=True)[:3]
        return PostSerializer(recent_posts, many=True, context=self.context).data

class BusinessCreateSerializer(serializers.ModelSerializer):
    town_id = serializers.UUIDField(write_only=True)
    category_id = serializers.UUIDField(write_only=True, required=False)
    
    class Meta:
        model = Business
        fields = ('name', 'description', 'town_id', 'category_id', 'address',
                 'phone', 'email', 'website', 'hero_image', 'logo', 'business_hours')
    
    def create(self, validated_data):
        town_id = validated_data.pop('town_id')
        category_id = validated_data.pop('category_id', None)
        
        business = Business.objects.create(
            owner=self.context['request'].user,
            town_id=town_id,
            category_id=category_id,
            **validated_data
        )
        return business

# Post Serializers
class PostSerializer(serializers.ModelSerializer):
    business = BusinessSerializer(read_only=True)
    author = UserSerializer(read_only=True)
    is_liked = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Post
        fields = ('id', 'business', 'author', 'caption', 'post_type', 'image', 'video',
                 'tags', 'category', 'likes_count', 'comments_count', 'shares_count',
                 'views_count', 'is_featured', 'is_pinned', 'is_liked',
                 'created_at', 'published_at')
        read_only_fields = ('id', 'likes_count', 'comments_count', 'shares_count', 'views_count')
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(user=request.user, post=obj).exists()
        return False

class PostCreateSerializer(serializers.ModelSerializer):
    business_id = serializers.UUIDField(write_only=True)
    category_id = serializers.UUIDField(write_only=True, required=False)
    
    class Meta:
        model = Post
        fields = ('business_id', 'caption', 'post_type', 'image', 'video', 'tags', 'category_id')
    
    def create(self, validated_data):
        business_id = validated_data.pop('business_id')
        category_id = validated_data.pop('category_id', None)
        
        post = Post.objects.create(
            author=self.context['request'].user,
            business_id=business_id,
            category_id=category_id,
            **validated_data
        )
        return post

# Comment Serializers
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ('id', 'user', 'content', 'parent', 'replies', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True, context=self.context).data
        return []

# Chat & Message Serializers
class ChatSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    business = BusinessSerializer(read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Chat
        fields = ('id', 'participants', 'business', 'chat_type', 'last_message',
                 'unread_count', 'is_active', 'created_at', 'updated_at')
    
    def get_last_message(self, obj):
        last_message = obj.messages.last()
        if last_message:
            return MessageSerializer(last_message, context=self.context).data
        return None
    
    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.messages.filter(is_read=False).exclude(sender=request.user).count()
        return 0

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ('id', 'sender', 'content', 'message_type', 'attachment',
                 'is_read', 'read_at', 'created_at', 'updated_at')
        read_only_fields = ('id', 'is_read', 'read_at', 'created_at', 'updated_at')

# Notification Serializers
class NotificationSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    related_business = BusinessSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = ('id', 'notification_type', 'title', 'message', 'sender',
                 'related_business', 'is_read', 'created_at', 'read_at')
        read_only_fields = ('id', 'created_at', 'read_at')


