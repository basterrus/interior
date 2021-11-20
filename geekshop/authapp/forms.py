import hashlib
from datetime import datetime
import pytz
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms

from authapp.models import UserProfile


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = UserProfile
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ('username', 'first_name', 'last_name', 'age', 'avatar', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def clean_age(self):
        yang = self.cleaned_data['age']
        if yang < 18:
            raise forms.ValidationError("Пользователь должен быть старше 18 лет!")
        return yang

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.is_active = False

        user.activate_key = hashlib.sha1(user.email.encode('utf-8')).hexdigest()
        user.activate_key_expired = datetime.now(pytz.timezone(settings.TIME_ZONE))

        user.save()
        return user


class ShopUserEditForm(UserChangeForm):
    class Meta:
        model = UserProfile
        fields = ('username', 'first_name', 'last_name', 'age', 'avatar', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()

    def clean_age(self):
        yang = self.cleaned_data['age']
        if yang < 18:
            raise forms.ValidationError("Пользователь должен быть старше 18 лет!")
        return yang
