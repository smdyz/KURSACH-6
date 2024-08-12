from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib import auth

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='E-mail')

    phone = models.CharField(max_length=35, verbose_name='Телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    country = models.CharField(max_length=25, verbose_name='Страна', **NULLABLE)
    is_verified = models.BooleanField(default=False, verbose_name='Подтверждён')
    token = models.CharField(max_length=10, verbose_name='Токен', **NULLABLE)
    is_blocked = models.BooleanField(default=False, verbose_name='Заблокирован')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}: {self.country}, {self.is_verified}, {self.is_blocked}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            (
                'can_block',
                'заблокировать'
            )
        ]


def auth_users(*args, **kwargs):
    return auth.models.User.objects.all().count()
