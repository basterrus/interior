from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
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

    def yang_age(self):
        yang = self.cleaned_data['age']
        if yang < 18:
            raise forms.ValidationError("Вы слишком молоды!")

        return yang


class ShopUserEditForm(UserChangeForm):
    model = UserProfile
    fields = ('username', 'first_name', 'last_name', 'email', 'age', 'avatar', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

            if field_name == 'password':
                field.widget = forms.HiddenInput()

    def yang_age(self):
        yang = self.cleaned_data['age']
        if yang < 18:
            raise forms.ValidationError("Вы слишком молоды!")

        return yang
