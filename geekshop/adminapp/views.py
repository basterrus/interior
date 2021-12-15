from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.db.models import F
from authapp.models import UserProfile
from authapp.forms import UserRegisterForm
from mainapp.models import ProductCategory, Product
from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse


class AccessMixin:
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserListView(AccessMixin, ListView):
    model = UserProfile
    template_name = 'adminapp/adminapp_users_list.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['title'] = 'Админ панель | Пользователи'
        return context


class UserCreateView(AccessMixin, CreateView):
    model = UserProfile
    template_name = 'adminapp/adminapp_user_edit_apdate_form.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('admins:admins_user')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Панель Администратора | Регистрация'
        return context


class UserUpdateView(AccessMixin, UpdateView):
    model = UserProfile
    template_name = 'adminapp/adminapp_user_edit_apdate_form.html'
    form_class = ShopUserAdminEditForm
    success_url = reverse_lazy('adminapp:users_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Панель Администратора | Обновление пользователя'
        return context


class UserDeleteView(AccessMixin, DeleteView):
    model = UserProfile
    template_name = 'adminapp/adminapp_user_delete.html'
    success_url = reverse_lazy('adminapp:users_list')


class CategoryListView(AccessMixin, ListView):
    model = ProductCategory
    template_name = 'adminapp/admiapp_categories.html'
    context_object_name = 'categories'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['title'] = 'Панель Администратора | Категории'
        return context


class CategoryCreateView(AccessMixin, CreateView):
    model = ProductCategory
    template_name = 'adminapp/adminapp_category_create.html'
    form_class = ProductCategoryEditForm

    def get_success_url(self):
        return reverse('adminapp:category_list', args=self.kwargs.get('pk'))

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Панель Администратора | Добавление категории'
        return context


class CategoryUpdateView(AccessMixin, UpdateView):
    model = ProductCategory
    template_name = 'adminapp/adminapp_category_create.html'
    form_class = ProductCategoryEditForm
    success_url = reverse_lazy('adminapp:category_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Панель Админимтратора | Обновление категории'
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data.get('discount')
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
        return super(CategoryUpdateView, self).form_valid(form)


class CategoryDeleteView(AccessMixin, DeleteView):
    model = ProductCategory
    template_name = 'adminapp/adminapp_delete_category.html'
    success_url = reverse_lazy('adminapp:category_list')


class ProductListView(AccessMixin, ListView):
    model = Product
    template_name = 'adminapp/admiapp_products_list.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['category'] = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))
        context_data['title'] = 'Панель Администратора | Список товаров'
        return context_data

    def get_queryset(self):
        return Product.objects.filter(category__pk=self.kwargs.get('pk'))


class ProductCreate(AccessMixin, CreateView):
    model = Product
    template_name = 'adminapp/adminapp_product_create.html'
    form_class = ProductEditForm

    def get_success_url(self):
        return reverse('adminapp:products_list', args=[self.kwargs['pk']])


class ProductUpdate(AccessMixin, UpdateView):
    model = Product
    template_name = 'adminapp/adminapp_product_create.html'
    form_class = ProductEditForm

    def get_success_url(self):
        product_item = Product.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:products_list', args=[product_item.category_id])


class ProductDelete(AccessMixin, DeleteView):
    model = Product
    template_name = 'adminapp/adminapp_delete_products.html'

    def get_success_url(self):
        product_item = Product.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:products_list', args=[product_item.category_id])


class ProductDetail(AccessMixin, DetailView):
    model = Product
    template_name = 'adminapp/adminapp_product_detail.html'
    context_object_name = 'objects_list'
