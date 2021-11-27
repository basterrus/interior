from django.forms import forms
from models import Product


class ProductForm(forms.Form):
    class Meta:
        model = Product
        fields = []

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
