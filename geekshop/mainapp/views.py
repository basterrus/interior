from django.shortcuts import render

links_menu = [
    {
        'url': 'products',
        'title': 'Все'
    },
    {
        'url': 'products_home',
        'title': 'Дом'
    },
    {
        'url': 'products_modern',
        'title': 'Модерн'
    },
    {
        'url': 'products_office',
        'title': 'Оффис'
    },
    {
        'url': 'products_classic',
        'title': 'Классика'
    }
]


# Create your views here.
def main(request):
    context = {
        'links_menu': links_menu,
        'title': 'Главная'
    }
    return render(request, 'mainapp/index.html', context=context)


def contact(request):
    context = {
        'links_menu': links_menu,
        'title': 'Контакты'
    }
    return render(request, 'mainapp/contact.html', context=context)


def products(request):
    context = {
        'links_menu': links_menu,
        'title': 'Продукты'
    }
    return render(request, 'mainapp/products.html', context=context)


def products_home(request):
    context = {
        'links_menu': links_menu,
        'title': 'Продукты для дома'
    }
    return render(request, 'mainapp/products.html', context=context)


def products_modern(request):
    context = {
        'links_menu': links_menu,
        'title': 'Продукты модерн'
    }
    return render(request, 'mainapp/products.html', context=context)


def products_office(request):
    context = {
        'links_menu': links_menu,
        'title': 'Продукты для офиса'
    }
    return render(request, 'mainapp/products.html', context=context)


def products_classic(request):
    context = {
        'links_menu': links_menu,
        'title': 'Продукты классика'
    }
    return render(request, 'mainapp/products.html', context=context)
