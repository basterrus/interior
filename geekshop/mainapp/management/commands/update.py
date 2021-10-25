from django.core.management.base import BaseCommand

from authapp.models import UserProfile
from mainapp.models import ProductCategory, Product
import json


def load_json(file_name):
    with open(f'json_upload/{file_name}.json', 'r', encoding='utf-8') as file:
        return json.load(file)


def clear_db():
    ProductCategory.objects.all().delete()
    Product.objects.all().delete()
    print('База очищена!')


class Command(BaseCommand):

    def handle(self, *args, **options):
        clear_db()

        categories = load_json('categories')
        products = load_json('products')
        try:
            for category in categories:
                ProductCategory.objects.create(**category)

            for product in products:
                category_name = product["category"]
                category_item = ProductCategory.objects.get(name=category_name)
                product["category"] = category_item
                Product.objects.create(**product)

        except Exception:
            print('Какая та ошибка')

        super_user = UserProfile.objects.create_superuser('django', 'django@geekshop.local', 'geekbrains', age=18)
        print(f'Пользователь {super_user} создан успешно!')
