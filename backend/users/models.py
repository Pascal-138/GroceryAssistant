from django.contrib.auth.models import AbstractUser

from django.db import models


class User(AbstractUser):
    """Модель пользователя."""

    username = models.CharField(
        verbose_name='Логин',
        max_length=150,
        unique=True,

    )
    password = models.CharField(
        max_length=150,
        verbose_name='Пароль',
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='Адрес электронной почты',
        unique=True,
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username


class Follow(models.Model):
    """Модель подписок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='is_subscribed',
        verbose_name='Подписчик'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['-author_id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_followers'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='follow_user_following_check'
            )
        ]

    def __str__(self) -> str:
        return (f'Пользователь {self.user}'
                f'оформил подписку на пользователя {self.author}')
