import json
import os
import random
from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from basket.models import Basket
from django.shortcuts import render
from mainapp.models import Product, ProductCategory
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

JSON_PATH = 'json_upload'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='utf-8') as infile:
        print(infile)
        return json.load(infile)


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_ordered_by_price():
    if settings.LOW_CACHE:
        key = 'products_ordered_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_ordered_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by(
                'price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


def get_hot_product():
    products = get_products()
    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk).select_related()[
                    :3]
    return same_products


class MainView(ListView):
    form = Product
    template_name = 'mainapp/index.html'
    model = Product
    is_home = Q(category__name='дом')
    is_office = Q(category__name='офис')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Главная страница'
        context_data['popular_product'] = Product.objects.filter(self.is_home | self.is_office)
        return context_data


def contacts_list(request):
    if settings.LOW_CACHE:
        key = f'locations'
        locations = cache.get(key)
        if locations is None:
            locations = load_from_json('contact')
            cache.set(key, locations)
    else:
        locations = load_from_json('contact')

    context = {
        'title': 'Контакты',
        'locations': locations,
    }
    return render(request, 'mainapp/contact.html', context)


@cache_page(3600)
def products(request, pk=None, page=1):
    title = 'Продукты'
    links_menu = get_links_menu()
    if pk is not None:
        if pk == 0:
            product_list = Product.objects.all()

            category = {
                'name': 'все',
                'pk': 0,
            }
        else:
            category = get_category(pk)
            product_list = get_products_in_category_ordered_by_price(pk)

        paginator = Paginator(product_list, 2)

        try:
            product_paginator = paginator.page(page)
        except PageNotAnInteger:
            product_paginator = paginator.page(1)
        except EmptyPage:
            product_paginator = paginator.page(paginator.num_pages)

        context = {
            'links_menu': links_menu,
            'title': 'Продукты',
            'product_list': product_paginator,
            'category': category,
        }

        return render(request, 'mainapp/products_list.html', context=context)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    context = {
        'links_menu': links_menu,
        'title': title,
        'hot_product': hot_product,
        'same_products': same_products,
    }

    return render(request, 'mainapp/products.html', context=context)


def product(request, pk):
    title = 'Продукты'
    links_menu = get_links_menu()
    product = get_product(pk)
    context = {
        'title': title,
        'product': product,
        'links_menu': links_menu,
    }

    return render(request, 'mainapp/product.html', context)


#
# class ProductsListViewAjax(ListView):
#     model = Product
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(ProductsListViewAjax, self).get_context_data(**kwargs)
#         context['product_list'] = get_products_ordered_by_price()
#


# def products_ajax(request, pk=None, page=1):
#     if request.is_ajax():
#         links_menu = get_links_menu()
#
#         if pk:
#             if pk == '0':
#                 category = {
#                     'pk': 0,
#                     'name': 'все'
#                 }
#                 product_list = get_products_ordered_by_price()
#             else:
#                 category = get_category(pk)
#                 product_list = get_products_in_category_ordered_by_price(pk)
#
#             paginator = Paginator(product_list, 2)
#
#             try:
#                 products_paginator = paginator.page(page)
#             except PageNotAnInteger:
#                 products_paginator = paginator.page(1)
#             except EmptyPage:
#                 products_paginator = paginator.page(paginator.num_pages)
#
#             content = {
#                 'links_menu': links_menu,
#                 'category': category,
#                 'products': products_paginator,
#             }
#
#             result = render_to_string(
#                 'mainapp/includes/inc_products_list_content.html',
#                 context=content,
#                 request=request)
#
#             return JsonResponse({'result': result})
