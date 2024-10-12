from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')

    avatar = models.ImageField(upload_to='media/avatars/%Y/%m', blank=True, null=True)
    phone = models.CharField(max_length=35, verbose_name='Телефон')
    country = models.CharField(max_length=50, verbose_name='Страна', blank=True, null=True)

    token = models.CharField(max_length=100, verbose_name='Токен', blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

