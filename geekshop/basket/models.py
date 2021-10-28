from django.db import models
from django.conf import settings
from mainapp.models import Product, ProductCategory


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    add_datatime = models.DateTimeField(auto_now_add=True)
    # update_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        # ordering = ('-id',)

    def __str__(self):
        return f'Корзина пользователя {self.user.name} | Продукт {self.product.name}'

    def sum(self):
        return self.quantity * self.product.price
