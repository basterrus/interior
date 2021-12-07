from django.urls import path, include
from mainapp import views as mainapp


app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.MainView.as_view(), name='index'),

    path('category/<int:pk>/', mainapp.products, name='category'),
    path('category/<int:pk>/<int:page>', mainapp.products, name='category_page'),

    path('', mainapp.products, name='products'),
    path('product/<int:pk>/', mainapp.product, name='product'),

]
