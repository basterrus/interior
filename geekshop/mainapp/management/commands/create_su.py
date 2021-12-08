from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username="root").exists():
            User.objects.create_superuser(
                "root", "admin@domain.com", "adminadmin", age=18)
            self.stdout.write(self.style.SUCCESS('Admin user has created'))
        else:
            self.stdout.write(self.style.SUCCESS('Admin user already exists'))
