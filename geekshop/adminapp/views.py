from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from authapp.models import UserProfile
from authapp.forms import UserRegisterForm
from mainapp.models import ProductCategory, Product
from django.contrib.auth.decorators import user_passes_test
from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm

from django.urls import reverse


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST, request.FILES)

        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:users_list'))


    else:
        user_form = UserRegisterForm()

    context = {
        'user_form': user_form,
    }

    return render(request, 'adminapp/user_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    title = 'Админ панель'

    context = {
        'object_list': UserProfile.objects.all().order_by('-is_active'),
        'title': title,
    }

    return render(request, 'adminapp/users.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    title = 'пользователи/редактирование'

    edit_user = get_object_or_404(UserProfile, pk=pk)
    if request.method == 'POST':
        user_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:users_list'))
    else:
        user_form = ShopUserAdminEditForm(instance=edit_user)

    content = {'title': title, 'user_form': user_form}

    return render(request, 'adminapp/user_form.html', content)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    delete_user = get_object_or_404(UserProfile, pk=pk)

    if request.method == 'POST':
        delete_user.delete()
        return HttpResponseRedirect(reverse('adminapp:users_list'))

    context = {
        'object': delete_user,
    }

    return render(request, 'adminapp/user_del.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    if request.method == 'POST':
        object_list = ProductCategoryEditForm(request.POST, request.FILES)
        object_list.save()
        return HttpResponseRedirect(reverse('adminapp:category_list'))
    else:
        object_list = ProductCategoryEditForm()

    context = {
        'title': 'Новая категория',
        'object_list': object_list,
    }

    return render(request, 'adminapp/category_create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    context = {
        'object_list': ProductCategory.objects.all().order_by('-is_active'),
        'title': 'Категории товаров',
    }

    return render(request, 'adminapp/categories.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    title = 'Категория/Редактировать'

    category_edit = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        new_cat = ProductCategoryEditForm(request.POST, request.FILES, instance=category_edit)
        if new_cat.is_valid():
            new_cat.save()
            return HttpResponseRedirect(reverse('adminapp:category_list'))
    else:
        new_cat = ProductCategoryEditForm(instance=category_edit)

    content = {
        'title': title,
        'object_list': new_cat,
    }

    return render(request, 'adminapp/category_create.html', content)


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    title = 'Категория/удалить'
    delete_cat = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        delete_cat.delete()
        return HttpResponseRedirect(reverse('adminapp:category_list'))

    context = {
        'object_list': delete_cat,
        'title': title,
    }

    return render(request, 'adminapp/delete_cat.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    if request.method == 'POST':
        object_list = ProductEditForm(request.POST, request.FILES)
        object_list.save()
        return HttpResponseRedirect(reverse('adminapp:category_list'))
    else:
        object_list = ProductEditForm()

    context = {
        'title': 'Новая категория',
        'object_list': object_list,
    }
    return render(request, 'adminapp/product_create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    context = {
        'category': get_object_or_404(ProductCategory, pk=pk),
        'object_list': Product.objects.filter(category__pk=pk).order_by('-is_active'),
    }

    return render(request, 'adminapp/pruducts.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    title = 'Товар/Редактировать'

    product_edit = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        object_list = ProductEditForm(request.POST, request.FILES, instance=product_edit)
        if object_list.is_valid():
            object_list.save()
            return HttpResponseRedirect(reverse('adminapp:category_list'))
    else:
        object_list = ProductEditForm(instance=product_edit)

    context = {
        'title': title,
        'object_list': object_list,
    }
    return render(request, 'adminapp/product_create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    title = 'Товар/удалить'

    delete_pr = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        delete_pr.delete()
        return HttpResponseRedirect(reverse('adminapp:category_list'))

    context = {
        'object_list': delete_pr,
        'title': title,
    }

    return render(request, 'adminapp/delete_pr.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_detail(request, pk):
    title = 'Товар/Информация'

    product_info = Product.objects.filter(category__pk=pk)
    context = {
        # 'category': get_object_or_404(ProductCategory, pk=pk),
        'object_list': Product.objects.filter(pk=pk).order_by('-is_active'),
        'title': 'Карточка товара'
    }
    return render(request, 'adminapp/product_detail.html', context)
