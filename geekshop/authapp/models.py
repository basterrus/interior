from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


# from django.core.exceptions import ValidationError


class UserProfile(AbstractUser):
    avatar = models.ImageField(upload_to='avatar', blank=True, verbose_name='Аватар')
    age = models.PositiveIntegerField(verbose_name='Возраст', blank=True)
    is_superuser = models.BooleanField(default=False, verbose_name='Администратор')

    activate_key = models.CharField(max_length=128, verbose_name='Код активации', blank=True, null=True)
    activate_key_expired = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователь'

    def is_activation_key_expired(self):
        if datetime.now(pytz.timezone(settings.TIME_ZONE)) > self.activate_key_expired + timedelta(hours=48):
            return True
        return False

    def activate_user(self):
        self.is_active = True
        self.activate_key = None
        self.activate_key_expired = None
        self.save()
