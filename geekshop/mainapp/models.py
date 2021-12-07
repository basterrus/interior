from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(verbose_name='Наименование', max_length=64, unique=True)
    description = models.TextField(verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Запись активна')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категория'
        ordering = ('-id',)


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField(max_length=128, verbose_name='Наименование')
    image = models.ImageField(upload_to='products', blank=True, verbose_name='Изображение')
    short_desc = models.CharField(max_length=255, verbose_name='Краткое описание')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0, verbose_name='Цена')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    is_active = models.BooleanField(default=True, verbose_name='Запись активна')

    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'{self.name} ({self.category.name})'

    class Meta:
        verbose_name = 'Продукты'
        verbose_name_plural = 'Продукты'
        ordering = ('-id',)

    @staticmethod
    def get_items():
        return Product.objects.filter(is_active=True). \
            order_by('category', 'name')
