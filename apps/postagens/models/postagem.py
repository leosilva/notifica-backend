from django.db import models

from apps.accounts.models import Usuario


class Postagem(models.Model):
    titulo = models.CharField(max_length=128)
    corpo = models.CharField(max_length=324)
    publicado_em = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    disponivel = models.BooleanField(default=True)  # type: ignore
