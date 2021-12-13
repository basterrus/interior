from django.db import models
from django.conf import settings
from django.utils.functional import cached_property
from mainapp.models import Product, ProductCategory


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, verbose_name='количество')
    add_datatime = models.DateTimeField(auto_now_add=True,
                                        verbose_name='время')  # TODO Заменить название поля на add_datetime

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'

    # def __str__(self):
    #     return f'Корзина пользователя {self.user.name} | Продукт {self.product.name}'

    @cached_property
    def items_cached(self):
        return self.user.basket.select_related()

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        _items = self.items_cached
        return sum(list(map(lambda x: x.quantity, _items)))

    @property
    def total_cost(self):
        _items = self.items_cached
        return sum(list(map(lambda x: x.product_cost, _items)))

    @property
    def get_item(self):
        return Basket.objects.filter(user=self.user)
