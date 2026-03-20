from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.postagens.views import PostagemViewSet


router = DefaultRouter()
router.register(r'postagem', PostagemViewSet)

urlpatterns = []
urlpatterns += router.urls
