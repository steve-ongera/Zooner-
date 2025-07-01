

# ============================================================================
# URLS.PY - URL routing for all API endpoints
# ============================================================================

from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Authentication URLs
    path('auth/login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/profile/', views.ProfileView.as_view(), name='profile'),
    
    # Towns & Categories
    path('towns/', views.TownListView.as_view(), name='town-list'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    
    # Business URLs
    path('businesses/', views.BusinessListView.as_view(), name='business-list'),
    path('businesses/create/', views.BusinessCreateView.as_view(), name='business-create'),
    path('businesses/my/', views.MyBusinessesView.as_view(), name='my-businesses'),
    path('businesses/<slug:slug>/', views.BusinessDetailView.as_view(), name='business-detail'),
    path('businesses/<uuid:business_id>/follow/', views.FollowBusinessView.as_view(), name='follow-business'),
    path('businesses/<uuid:business_id>/posts/', views.BusinessPostsView.as_view(), name='business-posts'),
    
    # Post URLs
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('posts/create/', views.PostCreateView.as_view(), name='post-create'),
    path('posts/<uuid:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/<uuid:post_id>/like/', views.LikePostView.as_view(), name='like-post'),
    path('posts/<uuid:post_id>/comments/', views.CommentListView.as_view(), name='post-comments'),
    path('posts/<uuid:post_id>/comments/create/', views.CommentCreateView.as_view(), name='create-comment'),
    
    # Chat URLs
    path('chats/', views.ChatListView.as_view(), name='chat-list'),
    path('chats/<uuid:pk>/', views.ChatDetailView.as_view(), name='chat-detail'),
    path('chats/<uuid:chat_id>/messages/', views.MessageListView.as_view(), name='chat-messages'),
    path('chats/<uuid:chat_id>/messages/create/', views.MessageCreateView.as_view(), name='create-message'),
    
    # Notification URLs
    path('notifications/', views.NotificationListView.as_view(), name='notification-list'),
    path('notifications/<uuid:notification_id>/read/', views.MarkNotificationReadView.as_view(), name='mark-notification-read'),
    
    # Search & Dashboard
    path('search/', views.SearchView.as_view(), name='search'),
    path('dashboard/stats/', views.DashboardStatsView.as_view(), name='dashboard-stats'),
]