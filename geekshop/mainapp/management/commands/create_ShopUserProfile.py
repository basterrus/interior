from django.core.management.base import BaseCommand

from authapp.models import UserProfile, ShopUserProfile


class Command(BaseCommand):

    def handle(self, *args, **options):
        users = UserProfile.objects.all()
        for user in users:
            ShopUserProfile.objects.create(user=user)
