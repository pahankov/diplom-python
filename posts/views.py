from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, UserSerializer
from .permissions import IsAuthorOrReadOnly

def index(request):
    """Главная страница с документацией API"""
    return render(request, 'posts/index.html')

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        
        if post.likes.filter(user=user).exists():
            post.likes.filter(user=user).delete()
            return Response({'status': 'unliked'})
        else:
            Like.objects.create(post=post, user=user)
            return Response({'status': 'liked'})

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    
    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_pk'])
    
    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post_id=self.kwargs['post_pk']
        )

class LikeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
