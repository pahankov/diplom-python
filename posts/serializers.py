from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment, Like


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']
        read_only_fields = ['id']


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'created_at']
        read_only_fields = ['id', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'text', 'image', 'created_at', 'comments', 'likes_count', 'liked']
        read_only_fields = ['id', 'created_at', 'likes_count', 'liked']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Like
        fields = ['id', 'user', 'created_at']
        read_only_fields = ['user', 'created_at']
