from django.urls import path
from adminapp import views as admin_views

app_name = 'adminapp'

urlpatterns = [
    path('users/create/', admin_views.UserCreateView.as_view(), name='user_create'),
    path('users/', admin_views.UserListView.as_view(), name='users_list'),
    path('users/update/<int:pk>/', admin_views.UserUpdateView.as_view(), name='user_update'),
    path('users/delete/<int:pk>/', admin_views.UserDeleteView.as_view(), name='user_delete'),

    path('categories/create/', admin_views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/', admin_views.CategoryListView.as_view(), name='category_list'),
    path('categories/update/<int:pk>/', admin_views.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', admin_views.CategoryDeleteView.as_view(), name='category_delete'),

    path('product/create/<int:pk>', admin_views.ProductCreate.as_view(), name='product_create'),
    path('products/<int:pk>/', admin_views.ProductListView.as_view(), name='products_list'),
    path('product/update/<int:pk>/', admin_views.ProductUpdate.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', admin_views.ProductDelete.as_view(), name='product_delete'),
    path('product/detail/<int:pk>/', admin_views.ProductDetail.as_view(), name='product_detail'),

]
