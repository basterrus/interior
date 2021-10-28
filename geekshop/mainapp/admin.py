from django.contrib import admin
from mainapp.models import Product, ProductCategory


class MaAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'short_desc', 'price', 'quantity')
    list_display_links = ('name',)
    search_fields = ('name', 'short_desc')


admin.site.register(Product, MaAdmin)
# admin.site.register(Product)
admin.site.register(ProductCategory)
