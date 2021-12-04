from django.shortcuts import render
from mainapp.models import Product, ProductCategory


def main(request):
    context = {
        'title': 'Главная',
        'links_menu': Product.objects.all()[:4],
    }
    return render(request, 'mainapp/index.html', context=context)


def contact(request):
    context = {
        'title': 'Контакты',
    }
    return render(request, 'mainapp/contact.html', context=context)


def products(request, pk=None):
    context = {
        'links_menu': ProductCategory.objects.all(),
        'title': 'Продукты'
    }
    return render(request, 'mainapp/products.html', context=context)
