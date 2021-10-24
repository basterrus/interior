
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
import mainapp.views as mainapp
import authapp.views as authapp

urlpatterns = [
    path('', mainapp.main, name='main'),
    path('products/', include('mainapp.urls', namespace='products')),
    path('contact/', mainapp.contact, name='contact'),
    path('login/', include('authapp.login', namespace='login')),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
