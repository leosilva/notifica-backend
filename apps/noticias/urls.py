from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.noticias.views import NoticiaViewSet

router = DefaultRouter()
router.register(r'noticia', NoticiaViewSet)

urlpatterns = []
urlpatterns += router.urls
