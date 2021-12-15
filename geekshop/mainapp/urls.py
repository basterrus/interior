from django.urls import path, include, re_path
from django.views.decorators.cache import cache_page
from mainapp import views as mainapp


app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.MainView.as_view(), name='index'),
    path('category/<int:pk>/', mainapp.products, name='category'),
    path('', mainapp.products, name='products'),
    path('product/<int:pk>/', mainapp.product, name='product'),
    path('category/<int:pk>/<int:page>', mainapp.products, name='category_page'),

    # path('category/<int:pk>/$', cache_page(3600)(mainapp.products)),
    # path(r'^category//page/(?P<page>\d+)/ajax/$', cache_page(3600)(mainapp.products_ajax)),

]
