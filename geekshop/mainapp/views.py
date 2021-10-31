import random

from basket.models import Basket
from django.shortcuts import render
from mainapp.models import Product, ProductCategory
from django.shortcuts import get_object_or_404


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def get_hot_product():
    products = Product.objects.all()
    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products


def main(request):
    context = {
        'title': 'Главная',
        'links_menu': Product.objects.all()[:4],
        'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/index.html', context=context)


def contact(request):
    context = {
        'title': 'Контакты',
        'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/contact.html', context=context)


def products(request, pk=None):
    title = 'Продукты'
    links_menu = ProductCategory.objects.all()
    basket = get_basket(request.user)
    if pk is not None:
        if pk == 0:
            product_list = Product.objects.all()
            category = {
                'name': 'все',
                'pk': 0,
            }
        else:
            product_list = Product.objects.filter(category__pk=pk)
            category = get_object_or_404(ProductCategory, pk=pk)
        context = {
            'links_menu': links_menu,
            'title': 'Продукты',
            'product_list': product_list,
            'category': category,
            'basket': get_basket(request.user),
        }

        return render(request, 'mainapp/products_list.html', context=context)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    context = {
        'links_menu': links_menu,
        'title': title,
        'hot_product':hot_product,
        'same_products': same_products,
        'basket': basket,
    }

    return render(request, 'mainapp/products.html', context=context)


def product(request, pk):
    title = 'Продукты'
    context = {
        'links_menu': ProductCategory.objects.all(),
        'title': title,
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(request.user),
    }

    return render(request, 'mainapp/product.html', context)