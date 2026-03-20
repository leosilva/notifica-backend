from django.contrib import admin
from django.urls import path, include
from core.views import healthcheck

urlpatterns = [
    path('api/', include('accounts.urls')),
    path('api/health/', healthcheck, name='healthcheck'),
]
