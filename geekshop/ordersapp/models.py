from django.conf import settings
from django.db import models
from mainapp.models import Product


class Order(models.Model):
    STATUS_FORMING = 'FM'
    STATUS_SENT_TO_PROCEED = 'STP'
    STATUS_PROCEEDED = 'PRD'
    STATUS_PAID = 'PD'
    STATUS_DONE = 'DN'
    STATUS_CANCELED = 'CN'

    STATUSES = (
        (STATUS_FORMING, 'формируется'),
        (STATUS_SENT_TO_PROCEED, 'отправлен в обработку'),
        (STATUS_PROCEEDED, 'обрабатывается'),
        (STATUS_PAID, 'оплачен'),
        (STATUS_DONE, 'готов к выдаче'),
        (STATUS_CANCELED, 'отменен'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now=True)
    status = models.CharField(verbose_name='статус', max_length=3, choices=STATUSES, default=STATUS_FORMING)
    is_active = models.BooleanField(verbose_name='активен', default=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Текущий заказ {self.id}'

    def get_total_quantity(self):
        _items = self.orderitems.all()
        return sum(list(map(lambda x: x.quantity, _items)))

    def get_product_type_quantity(self, *args, **kwargs):
        _items = self.orderitems.all()
        return len(_items)

    def get_total_cost(self, *args, **kwargs):
        _items = self.orderitems.all()
        return sum(list(map(lambda x: x.quantity * x.product.price, _items)))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='orderitems', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='продукт', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)

    class Meta:
        ordering = ('-order',)
        verbose_name = 'ордер'
        verbose_name_plural = 'ордеры'

    def __str__(self):
        return f'Текущий заказ {self.id}'

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.get(pk=pk)
