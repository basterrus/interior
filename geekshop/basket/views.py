from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from basket.models import Basket
from mainapp.models import Product
from django.template.loader import render_to_string
from django.http import JsonResponse


@login_required
def basket(request):
    basket_items = Basket.objects.filter(user=request.user)
    context = {
        'title': 'Корзина товаров',
        'basket_items': basket_items,
    }
    return render(request, 'basket/basket.html', context)


@login_required
def add(request, pk):
    product_item = get_object_or_404(Product, pk=pk)

    basket_item = Basket.objects.filter(product=product_item, user=request.user).first()

    if not basket_item:
        basket_item = Basket(product=product_item, user=request.user)
    basket_item.quantity += 1
    basket_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        basket_item = Basket.objects.get(pk=pk)

        if quantity > 0:
            basket_item.quantity = quantity
            basket_item.save()
        else:
            basket_item.delete()

    basket_item = Basket.objects.filter(user=request.user).select_related()

    context = {
        'basket_item': basket_item,
    }

    result = render_to_string('basket/includes/inc_basket_list.html', context)

    return JsonResponse({'result': result})
