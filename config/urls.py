"""
from django.contrib import admin
<<<<<<< HEAD
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls')),
    path('api/', include('categories.urls')),
    path('products/', include('products.urls')),
=======
from django.urls import path,include
from django.views.generic import TemplateView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('login.urls')),
    #Language setting
    path('i18n/', include('django.conf.urls.i18n')),
    path(
    'language/',
    TemplateView.as_view(template_name='language.html'),
    name='language_settings'
),
>>>>>>> f7777839f6849940ab24be38b4d4e7a6a2df30c1
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Login
    path('', include('login.urls')),

    # Categories
    path('api/', include('categories.urls')),

    # Products
    path('products/', include('products.urls')),

    # Language settings
    path('i18n/', include('django.conf.urls.i18n')),
    path(
        'language/',
        TemplateView.as_view(template_name='language.html'),
        name='language_settings'
    ),
    path("orders/", include("orders.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
