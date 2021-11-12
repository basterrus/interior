from django.conf import settings
from django import template

register = template.Library()


@register.filter(name='media_for_products')  # 1 вариант регистрации шаблонного тега
def media_for_products(img_path):
    if not img_path:
        img_path = 'default_prod.svg'

    return f'{settings.MEDIA_URL}{img_path}'


@register.filter(name='media_for_users')
def media_for_users(img_path):
    if not img_path:
        img_path = 'default_users.svg'

    return f'{settings.MEDIA_URL}{img_path}'

# register.filter('media_for_products', media_for_products) # менее предпочтительный 2 вариант регистрации шаблонного
# тега
