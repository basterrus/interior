from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from basket.models import Basket
from mainapp.models import Product


def view(request, pk=None):
    context = {
        'title': 'Корзина товаров'
    }
    return render(request, 'basket/basket.html', context=context)


def add(request, pk):
    product_item = get_object_or_404(Product, pk=pk)

    basket_item = Basket.objects.filter(product=product_item, user=request.user).first()

    if not basket_item:
        basket_item = Basket(product=product_item, user=request.user)
    basket_item.quantity += 1
    basket_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove(request, pk):
    Basket.objects.get(pk=pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
