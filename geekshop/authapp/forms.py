from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = UserProfile
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
