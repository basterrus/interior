from basket.models import Basket
from django.shortcuts import render
from mainapp.models import Product, ProductCategory
from django.shortcuts import get_object_or_404


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    return []


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

    same_products = Product.objects.all()[3:5]

    context = {
        'links_menu': links_menu,
        'title': title,
        'same_products': same_products

    }
    return render(request, 'mainapp/products.html', context=context)
