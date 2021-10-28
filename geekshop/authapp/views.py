from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import UserLoginForm, UserRegisterForm, ShopUserEditForm
from django.contrib import auth
from django.urls import reverse


def login(request):
    title = 'ВХОД'

    login_form = UserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main'))

    context = {
        'title': title,
        'login_form': login_form}

    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def register(request):
    title = 'Регистрация пользователя'

    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('main'))
    else:
        register_form = UserRegisterForm()

    context = {
        'register_form': register_form,
        'title': title,
    }

    return render(request, 'authapp/register.html', context)


def edit(request):
    title = 'Редактирование профиля'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)

    context = {
        'edit_form': edit_form,
        'title': title,
    }
    print(request.user)
    return render(request, 'authapp/edit.html', context)


def delete(request):
    return None
