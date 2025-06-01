from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    text = models.TextField(
        verbose_name='Текст публикации'
    )
    image = models.ImageField(
        upload_to='posts/',
        verbose_name='Изображение',
        blank=True
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-created_at']

    def __str__(self):
        return f'Публикация {self.author.username} от {self.created_at}'


# для дополнительного задания
# class PostImage(models.Model):
#     ...


class Like(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='Публикация'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='Пользователь'
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        unique_together = ['post', 'user']

    def __str__(self):
        return f'Лайк от {self.user.username} к публикации {self.post.id}'


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Публикация'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField(
        verbose_name='Текст комментария'
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']

    def __str__(self):
        return f'Комментарий {self.author.username} к публикации {self.post.id}'
