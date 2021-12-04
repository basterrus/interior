from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from basket.models import Basket
from ordersapp.forms import OrderItemForm
from ordersapp.models import Order, OrderItem
from django.forms.models import inlineformset_factory


class OrderItemsListView(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderItemsCreateView(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('order:order_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if basket_items.exists():
                OrderFormSet = inlineformset_factory(Order, OrderItem, OrderItemForm, extra=basket_items.count())
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
            else:
                formset = OrderFormSet()

        context_data['orderitems'] = formset
        print(context_data)
        return context_data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user  # Присваиваем пользователя
            self.object = form.save()
            if orderitems.is_valid():  # Проверка валидации
                orderitems.instance = self.object
                orderitems.save()

        # Удаление пустого заказа ОШИБКА RELAITEDNAMES
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderItemsUpdateView(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('order:order_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            formset = OrderFormSet()

        context_data['orderitems'] = formset
        return context_data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user  # Присваиваем пользователя
            self.object = form.save()
            if orderitems.is_valid():  # Проверка валидации
                orderitems.instance = self.object
                orderitems.save()

        # Удаление пустого заказа ОШИБКА RELAITEDNAMES заменил select_related() на all()
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderItemsDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('order:order_list')


class OrderItemsDetailView(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderItemsDetailView, self).get_context_data(**kwargs)
        return context


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.STATUS_SENT_TO_PROCEED
    order.save()
    return HttpResponseRedirect(reverse('order:order_list'))
