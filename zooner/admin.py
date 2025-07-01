from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Count
from django.utils import timezone
from .models import (
    User, Town, Category, Business, Post, Follow, Like, Comment,
    Chat, Message, Notification, UserEngagement, BusinessAnalytics,
    ReportedContent
)


# Custom User Admin
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'is_verified', 'is_active', 'last_active', 'created_at']
    list_filter = ['role', 'is_verified', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    readonly_fields = ['id', 'created_at', 'updated_at', 'last_login', 'date_joined']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile Information', {
            'fields': ('phone_number', 'bio', 'location', 'profile_image', 'role', 'is_verified')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'last_active'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            business_count=Count('owned_businesses')
        )


# Town Admin
@admin.register(Town)
class TownAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'region', 'business_count', 'is_active', 'created_at']
    list_filter = ['country', 'region', 'is_active']
    search_fields = ['name', 'country', 'region']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['id', 'created_at', 'business_count']
    
    def business_count(self, obj):
        return obj.businesses.count()
    business_count.short_description = 'Businesses'
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            business_count=Count('businesses')
        )


# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon_display', 'color_display', 'business_count', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['id', 'created_at', 'business_count']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'name']
    
    def icon_display(self, obj):
        if obj.icon:
            return format_html('<span style="font-size: 20px;">{}</span>', obj.icon)
        return '-'
    icon_display.short_description = 'Icon'
    
    def color_display(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #ccc;"></div>',
            obj.color
        )
    color_display.short_description = 'Color'
    
    def business_count(self, obj):
        return obj.businesses.count()
    business_count.short_description = 'Businesses'


# Business Admin
@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'town', 'category', 'status', 'is_verified', 'is_featured', 'followers_count', 'posts_count', 'created_at']
    list_filter = ['status', 'is_verified', 'is_featured', 'category', 'town', 'created_at']
    search_fields = ['name', 'description', 'owner__username', 'owner__email']
    readonly_fields = ['id', 'slug', 'created_at', 'updated_at', 'followers_count', 'posts_count']
    raw_id_fields = ['owner']
    list_editable = ['status', 'is_verified', 'is_featured']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'owner', 'description', 'category')
        }),
        ('Location', {
            'fields': ('town', 'address', 'latitude', 'longitude')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'website')
        }),
        ('Media', {
            'fields': ('hero_image', 'logo')
        }),
        ('Business Settings', {
            'fields': ('business_hours', 'status', 'is_featured', 'is_verified')
        }),
        ('Statistics', {
            'fields': ('followers_count', 'posts_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('owner', 'town', 'category')


# Post Admin
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['caption_short', 'business', 'author', 'post_type', 'likes_count', 'comments_count', 'is_active', 'is_featured', 'published_at']
    list_filter = ['post_type', 'is_active', 'is_featured', 'is_pinned', 'published_at', 'business__category']
    search_fields = ['caption', 'business__name', 'author__username']
    readonly_fields = ['id', 'created_at', 'updated_at', 'likes_count', 'comments_count', 'shares_count', 'views_count']
    raw_id_fields = ['business', 'author']
    list_editable = ['is_active', 'is_featured']
    date_hierarchy = 'published_at'
    
    def caption_short(self, obj):
        return obj.caption[:50] + '...' if len(obj.caption) > 50 else obj.caption
    caption_short.short_description = 'Caption'
    
    fieldsets = (
        ('Content', {
            'fields': ('business', 'author', 'caption', 'post_type', 'category')
        }),
        ('Media', {
            'fields': ('image', 'video')
        }),
        ('Metadata', {
            'fields': ('tags',)
        }),
        ('Settings', {
            'fields': ('is_active', 'is_featured', 'is_pinned', 'published_at')
        }),
        ('Metrics', {
            'fields': ('likes_count', 'comments_count', 'shares_count', 'views_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# Follow Admin
@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['user', 'business', 'created_at']
    list_filter = ['created_at', 'business__category']
    search_fields = ['user__username', 'business__name']
    readonly_fields = ['id', 'created_at']
    raw_id_fields = ['user', 'business']


# Like Admin
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post_link', 'created_at']
    list_filter = ['created_at', 'post__business__category']
    search_fields = ['user__username', 'post__business__name']
    readonly_fields = ['id', 'created_at']
    raw_id_fields = ['user', 'post']
    
    def post_link(self, obj):
        url = reverse('admin:zooner_post_change', args=[obj.post.id])
        return format_html('<a href="{}">{}</a>', url, str(obj.post)[:50])
    post_link.short_description = 'Post'


# Comment Admin
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post_link', 'content_short', 'is_reply', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at', 'post__business__category']
    search_fields = ['user__username', 'content', 'post__business__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['user', 'post', 'parent']
    list_editable = ['is_active']
    
    def content_short(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_short.short_description = 'Content'
    
    def post_link(self, obj):
        url = reverse('admin:zooner_post_change', args=[obj.post.id])
        return format_html('<a href="{}">{}</a>', url, str(obj.post)[:30])
    post_link.short_description = 'Post'
    
    def is_reply(self, obj):
        return obj.parent is not None
    is_reply.boolean = True
    is_reply.short_description = 'Reply'


# Chat Admin
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat_type', 'business', 'participant_list', 'is_active', 'updated_at']
    list_filter = ['chat_type', 'is_active', 'created_at']
    search_fields = ['business__name', 'participants__username']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['business']
    filter_horizontal = ['participants']
    
    def participant_list(self, obj):
        return ", ".join([user.username for user in obj.participants.all()[:3]])
    participant_list.short_description = 'Participants'


# Message Admin
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'chat_link', 'message_type', 'content_short', 'is_read', 'created_at']
    list_filter = ['message_type', 'is_read', 'created_at']
    search_fields = ['sender__username', 'content', 'chat__business__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['chat', 'sender']
    date_hierarchy = 'created_at'
    
    def content_short(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_short.short_description = 'Content'
    
    def chat_link(self, obj):
        url = reverse('admin:zooner_chat_change', args=[obj.chat.id])
        return format_html('<a href="{}">{}</a>', url, str(obj.chat)[:30])
    chat_link.short_description = 'Chat'


# Notification Admin
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'notification_type', 'title', 'is_read', 'is_sent', 'created_at']
    list_filter = ['notification_type', 'is_read', 'is_sent', 'created_at']
    search_fields = ['recipient__username', 'sender__username', 'title', 'message']
    readonly_fields = ['id', 'created_at', 'read_at']
    raw_id_fields = ['recipient', 'sender', 'related_post', 'related_business', 'related_chat']
    list_editable = ['is_sent']
    date_hierarchy = 'created_at'


# User Engagement Admin
@admin.register(UserEngagement)
class UserEngagementAdmin(admin.ModelAdmin):
    list_display = ['user', 'engagement_type', 'related_content', 'session_id', 'created_at']
    list_filter = ['engagement_type', 'created_at']
    search_fields = ['user__username', 'session_id']
    readonly_fields = ['id', 'created_at']
    raw_id_fields = ['user', 'related_post', 'related_business']
    date_hierarchy = 'created_at'
    
    def related_content(self, obj):
        if obj.related_post:
            return f"Post: {obj.related_post.business.name}"
        elif obj.related_business:
            return f"Business: {obj.related_business.name}"
        return "-"
    related_content.short_description = 'Related Content'


# Business Analytics Admin
@admin.register(BusinessAnalytics)
class BusinessAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['business', 'date', 'profile_views', 'post_views', 'new_followers', 'engagement_rate']
    list_filter = ['date', 'business__category']
    search_fields = ['business__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['business']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('business', 'date')
        }),
        ('View Metrics', {
            'fields': ('profile_views', 'post_views', 'reach')
        }),
        ('Engagement Metrics', {
            'fields': ('new_followers', 'total_likes', 'total_comments', 'total_shares', 'engagement_rate')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# Reported Content Admin
@admin.register(ReportedContent)
class ReportedContentAdmin(admin.ModelAdmin):
    list_display = ['reporter', 'report_type', 'reported_content', 'status', 'reviewed_by', 'created_at']
    list_filter = ['report_type', 'status', 'created_at']
    search_fields = ['reporter__username', 'reason', 'admin_notes']
    readonly_fields = ['id', 'created_at', 'reviewed_at']
    raw_id_fields = ['reporter', 'reported_post', 'reported_business', 'reported_user', 'reviewed_by']
    list_editable = ['status']
    
    def reported_content(self, obj):
        if obj.reported_post:
            return f"Post: {obj.reported_post.business.name}"
        elif obj.reported_business:
            return f"Business: {obj.reported_business.name}"
        elif obj.reported_user:
            return f"User: {obj.reported_user.username}"
        return "-"
    reported_content.short_description = 'Reported Content'
    
    fieldsets = (
        ('Report Details', {
            'fields': ('reporter', 'report_type', 'reason')
        }),
        ('Reported Content', {
            'fields': ('reported_post', 'reported_business', 'reported_user')
        }),
        ('Review', {
            'fields': ('status', 'admin_notes', 'reviewed_by', 'reviewed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if change and obj.status in ['reviewed', 'resolved', 'dismissed'] and not obj.reviewed_by:
            obj.reviewed_by = request.user
            obj.reviewed_at = timezone.now()
        super().save_model(request, obj, form, change)


# Customize Django Admin Site
admin.site.site_header = "Zooner Admin"
admin.site.site_title = "Zooner Admin Portal"
admin.site.index_title = "Welcome to Zooner Administration"