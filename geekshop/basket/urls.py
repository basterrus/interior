
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from basket import views as basket

app_name = 'basket'

urlpatterns = [
    path('', basket.view,  name='view'),
    path('add/<int:pk>/', basket.add, name='add'),
    path('remove/<int:pk>/', basket.remove, name='remove'),
    path('edit/<int:pk>/<int:quantity>/', basket.edit, name='edit'),
]