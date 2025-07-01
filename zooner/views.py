
# ============================================================================
# VIEWS.PY - API Views for all endpoints
# ============================================================================

from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from .serializers import *


# Authentication Views
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = User.objects.get(email=request.data['email'])
            user_data = UserSerializer(user).data
            response.data['user'] = user_data
        return response

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'message': 'User registered successfully',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

# Town Views
class TownListView(generics.ListAPIView):
    queryset = Town.objects.filter(is_active=True)
    serializer_class = TownSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'region']

# Category Views
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

# Business Views
class BusinessListView(generics.ListAPIView):
    serializer_class = BusinessSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['town', 'category', 'is_featured']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'followers_count']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Business.objects.filter(status='active')
        town_name = self.request.query_params.get('town_name', None)
        if town_name:
            queryset = queryset.filter(town__name__icontains=town_name)
        return queryset

class BusinessDetailView(generics.RetrieveAPIView):
    queryset = Business.objects.filter(status='active')
    serializer_class = BusinessSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

class BusinessCreateView(generics.CreateAPIView):
    serializer_class = BusinessCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        # Only business owners can create businesses
        if self.request.user.role != 'business':
            self.request.user.role = 'business'
            self.request.user.save()
        serializer.save()

class MyBusinessesView(generics.ListAPIView):
    serializer_class = BusinessSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Business.objects.filter(owner=self.request.user)

# Follow/Unfollow Business
class FollowBusinessView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, business_id):
        business = get_object_or_404(Business, id=business_id, status='active')
        follow, created = Follow.objects.get_or_create(user=request.user, business=business)
        
        if created:
            return Response({'message': 'Following business', 'following': True})
        else:
            follow.delete()
            return Response({'message': 'Unfollowed business', 'following': False})

# Post Views
class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['business', 'post_type', 'category']
    search_fields = ['caption', 'tags']
    ordering = ['-published_at']
    
    def get_queryset(self):
        queryset = Post.objects.filter(is_active=True)
        
        # Filter by town if provided
        town_name = self.request.query_params.get('town_name', None)
        if town_name:
            queryset = queryset.filter(business__town__name__icontains=town_name)
        
        # Get followed businesses posts for authenticated users
        following_only = self.request.query_params.get('following', None)
        if following_only and self.request.user.is_authenticated:
            followed_businesses = Follow.objects.filter(user=self.request.user).values_list('business', flat=True)
            queryset = queryset.filter(business__in=followed_businesses)
        
        return queryset

class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.filter(is_active=True)
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

class PostCreateView(generics.CreateAPIView):
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

class BusinessPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        business_id = self.kwargs['business_id']
        return Post.objects.filter(business_id=business_id, is_active=True)

# Like/Unlike Post
class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id, is_active=True)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if created:
            post.likes_count += 1
            post.save()
            return Response({'message': 'Post liked', 'liked': True, 'likes_count': post.likes_count})
        else:
            like.delete()
            post.likes_count -= 1
            post.save()
            return Response({'message': 'Post unliked', 'liked': False, 'likes_count': post.likes_count})

# Comment Views
class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id, parent=None, is_active=True)

class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)
        serializer.save(user=self.request.user, post=post)
        
        # Update comment count
        post.comments_count += 1
        post.save()

# Chat Views
class ChatListView(generics.ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Chat.objects.filter(participants=self.request.user, is_active=True)

class ChatDetailView(generics.RetrieveAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Chat.objects.filter(participants=self.request.user)

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        chat = get_object_or_404(Chat, id=chat_id, participants=self.request.user)
        return chat.messages.all()

class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        chat_id = self.kwargs['chat_id']
        chat = get_object_or_404(Chat, id=chat_id, participants=self.request.user)
        serializer.save(sender=self.request.user, chat=chat)

# Notification Views
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

class MarkNotificationReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, notification_id):
        notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()
        return Response({'message': 'Notification marked as read'})

# Search View
class SearchView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        query = request.query_params.get('q', '')
        town_name = request.query_params.get('town', '')
        
        if not query:
            return Response({'message': 'Query parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Search businesses
        businesses = Business.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            status='active'
        )
        
        if town_name:
            businesses = businesses.filter(town__name__icontains=town_name)
        
        # Search posts
        posts = Post.objects.filter(
            Q(caption__icontains=query) | Q(tags__icontains=query),
            is_active=True
        )
        
        if town_name:
            posts = posts.filter(business__town__name__icontains=town_name)
        
        return Response({
            'businesses': BusinessSerializer(businesses[:10], many=True).data,
            'posts': PostSerializer(posts[:10], many=True, context={'request': request}).data
        })

# Dashboard Stats (for business owners)
class DashboardStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        if request.user.role != 'business':
            return Response({'message': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
        
        businesses = Business.objects.filter(owner=request.user)
        total_followers = Follow.objects.filter(business__in=businesses).count()
        total_posts = Post.objects.filter(business__in=businesses).count()
        total_likes = Like.objects.filter(post__business__in=businesses).count()
        
        return Response({
            'total_businesses': businesses.count(),
            'total_followers': total_followers,
            'total_posts': total_posts,
            'total_likes': total_likes,
            'businesses': BusinessSerializer(businesses, many=True).data
        })