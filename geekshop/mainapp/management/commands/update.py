from django.core.management.base import BaseCommand
from mainapp.models import Product, ProductCategory
import json
from django.conf import settings
from authapp.models import UserProfile


def load_file(file_name):
    with open(f'{settings.BASE_DIR}/json_upload/{file_name}.json', 'r') as file:
        return json.load(file)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_file('categories')
        products = load_file('products')

        # Clear categories in DB and load new data from JSON
        ProductCategory.objects.all().delete()
        for category in categories:
            ProductCategory.objects.create(**category)

        # Clear products in DB and load new data from JSON
        Product.objects.all().delete()
        try:
            for product in products:
                category_name = product["category"]
                category_item = ProductCategory.objects.get(name=category_name)
                product["category"] = category_item
                Product.objects.create(**product)
        except Exception:
            print('какая то ошибка не могу понять? но в базу сохраняет')

        UserProfile.objects.create_superuser('django',  password='geekbrains', age=33)
