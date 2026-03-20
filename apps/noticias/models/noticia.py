from django.db import models
from apps.accounts.models import Usuario


class Noticia(models.Model):
    titulo = models.CharField(max_length=255)
    sumario = models.CharField(max_length=512)

    link = models.URLField(unique=True)
    imagem = models.URLField()

    data = models.DateField()
    disponivel = models.BooleanField(default=True)

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
