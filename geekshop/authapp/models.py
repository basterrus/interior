from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class UserProfile(AbstractUser):
    avatar = models.ImageField(upload_to='avatar', blank=True, verbose_name='Аватар')
    age = models.PositiveIntegerField(verbose_name='Возраст', blank=True)
    is_superuser = models.BooleanField(default=False, verbose_name='Администратор')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователь'
        # abstract = True
