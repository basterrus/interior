from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
import mainapp.views as mainapp

urlpatterns = [
    path('', mainapp.MainView.as_view(), name='main'),
    path('', include('social_django.urls', namespace='social')),
    path('products/', include('mainapp.urls', namespace='products')),
    path('contacts/', mainapp.contacts_list, name='contact'),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('auth/', include('authapp.urls', namespace='register')),
    path('basket/', include('basket.urls', namespace='basket')),
    path('admin/', include('adminapp.urls', namespace='adminapp')),

    path('control/', admin.site.urls),

    path('order/', include('ordersapp.urls', namespace='order')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [re_path(r'^__debug__/', include(debug_toolbar.urls))]
