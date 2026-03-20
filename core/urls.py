from django.urls import path, include
from core.views import healthcheck
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('api/', include('apps.accounts.urls')),
    path('api/', include('apps.noticias.urls')),
    path('api/', include('apps.postagens.urls')),
    path('api/', include('apps.carrossel.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')),

    path('api/health/', healthcheck, name='healthcheck'),
]
