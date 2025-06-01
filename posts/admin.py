from django.contrib import admin
from .models import Post, Comment, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('text', 'author__username')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'text', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('text', 'author__username', 'post__text')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('user__username', 'post__text')
