import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from basket.models import Basket
from django.shortcuts import render
from mainapp.models import Product, ProductCategory
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator


def get_hot_product():
    products = Product.objects.all()
    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk).select_related()[:3]
    return same_products


class MainView(ListView):
    form = Product
    template_name = 'mainapp/index.html'
    model = Product

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Главная страница'
        context_data['popular_product'] = Product.objects.all()[:4]
        return context_data


def contacts_list(request):
    context = {
        'title': 'Контакты',
    }
    return render(request, 'mainapp/contact.html', context)

#
# class ProductsView(ListView):
#     form = Product
#     template_name = 'mainapp/products_list.html'
#
#     def get_queryset(self):
#         return super(ProductsView, self).get_queryset().all()
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(ProductsView, self).get_context_data(**kwargs)
#         context['title'] = 'Товары'
#         pk = get_object_or_404(Product, pk=self.kwargs.get('pk'))
#
#         if pk is not None:
#             if pk == 0:
#                 context['product_list'] = Product.objects.all()
#                 category = {
#                     'name': 'все',
#                     'pk': 0,
#                 }
#             else:
#                 category = get_object_or_404(ProductCategory, pk=pk)
#                 product_list = Product.objects.filter(category__pk=pk)
#
#         return context


def products(request, pk=None, page=1):
    print(pk)
    title = 'Продукты'
    links_menu = ProductCategory.objects.all()
    if pk is not None:
        if pk == 0:
            product_list = Product.objects.all()

            category = {
                'name': 'все',
                'pk': 0,
            }
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            product_list = Product.objects.filter(category__pk=pk)

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
    context = {
        'title': title,
        'product': get_object_or_404(Product, pk=pk),
    }

    return render(request, 'mainapp/product.html', context)
