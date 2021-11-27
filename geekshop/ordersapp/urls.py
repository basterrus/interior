from django.urls import path
from ordersapp import views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
    path('order/', ordersapp.OrderItemsListView.as_view(), name='order_list'),
    path('read/<pk>/', ordersapp.OrderItemsDetailView.as_view(), name='order_read'),
    path('create/', ordersapp.OrderItemsCreateView.as_view(), name='order_create'),
    path('update/<pk>/', ordersapp.OrderItemsUpdateView.as_view(), name='order_update'),
    path('delete/<pk>/', ordersapp.OrderItemsDeleteView.as_view(), name='order_delete'),
    path('complete/<pk>/', ordersapp.order_forming_complete, name='complete'),

]
