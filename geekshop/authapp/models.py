from datetime import datetime, timedelta
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import pytz
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    avatar = models.ImageField(upload_to='avatar', blank=True, verbose_name='Аватар')
    age = models.PositiveIntegerField(verbose_name='Возраст', blank=True, default=18)
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


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'
    OTHERS = 'O'

    GENDERS = (
        (MALE, 'Мужской'),
        (FEMALE, 'Женский'),
        (OTHERS, 'Другое'),
    )

    user = models.OneToOneField(UserProfile, null=False, unique=True, on_delete=models.CASCADE, db_index=True)
    tagline = models.CharField(max_length=128, verbose_name='Тэги', blank=True)
    about_me = models.TextField(verbose_name='Обо мне')
    gender = models.CharField(choices=GENDERS, default=OTHERS, verbose_name='Пол', max_length=1)

    @receiver(post_save, sender=UserProfile)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=UserProfile)
    def update_user_profile(sender, instance, created, **kwargs):
        instance.shopuserprofile.save()
