from django.urls import path
from apps.carrossel.views import CarrosselView

urlpatterns = [
    path('carrossel/', CarrosselView.as_view())
]
