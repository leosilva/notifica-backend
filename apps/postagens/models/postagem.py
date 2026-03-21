from django.db import models
from apps.accounts.models import Usuario


class Postagem(models.Model):
    corpo = models.CharField(max_length=324)
    publicado_em = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
