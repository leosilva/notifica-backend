from django.contrib import admin
from django.urls import path, include
from core.views import healthcheck

urlpatterns = [
    path('api/', include('apps.accounts.urls')),
    path('api/', include('apps.noticias.urls')),
    path('api/health/', healthcheck, name='healthcheck'),
]
