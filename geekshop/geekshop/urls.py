
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
import mainapp.views as mainapp

urlpatterns = [
    path('', mainapp.main, name='main'),
    path('products/', include('mainapp.urls', namespace='products')),
    path('contact/', mainapp.contact, name='contact'),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('auth/', include('authapp.urls', namespace='register')),
    path('basket/', include('basket.urls', namespace='basket')),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
