import requests
from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import UserLoginForm, UserRegisterForm, ShopUserEditForm, ShopUserProfileEditForm
from django.contrib import auth
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail

from authapp.models import UserProfile
from authapp.services import send_verify_email


def login(request):
    title = 'Вход'

    login_form = UserLoginForm(data=request.POST)
    next = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main'))

    context = {
        'title': title,
        'login_form': login_form,
        'next': next,
    }

    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def register(request):

    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            if send_verify_email(user):
                print('сообщение подтверждения отправлено')
                return HttpResponseRedirect(reverse('auth:login'))
            else:
                print('ошибка отправки сообщения')
                return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = UserRegisterForm()

    context = {
        'register_form': register_form,
        'title': 'Регистрация пользователя',
    }

    return render(request, 'authapp/register.html', context)


def edit(request):
    if request.method == 'POST':

        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        edit_profile_form = ShopUserProfileEditForm(request.POST, instance=request.user.shopuserprofile)

        if edit_form.is_valid() and edit_profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('authapp:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        edit_profile_form = ShopUserProfileEditForm(instance=request.user.shopuserprofile)

    context = {
        'edit_form': edit_form,
        'title': 'Редактирование профиля',
        'edit_profile_form': edit_profile_form,
    }
    print(request.user)
    return render(request, 'authapp/edit.html', context)


# def delete(request):
#     return None


def verify(request, email, key):
    user = UserProfile.objects.filter(email=email).first()
    if user:
        if user.activate_key == key and not user.activate_key_expired():
            user.activate_user()
            auth.login(request, user)

    return render(request, 'authapp/register_socifull.html')





