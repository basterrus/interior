
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
import mainapp.views as mainapp

urlpatterns = [
    path('', mainapp.main, name='main'),
    path('products/', include('mainapp.urls', namespace='products')),
    path('contacts/', mainapp.contact, name='contact'),
    path('auth/', include('authapp.urls', namespace='auth')),
    # path('auth/', include('authapp.urls', namespace='register')),
    path('basket/', include('basket.urls', namespace='basket')),
    path('admin/', include('adminapp.urls', namespace='adminapp')),

    path('control/', admin.site.urls),

    path('', include('social_django.urls', namespace='social'))

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
