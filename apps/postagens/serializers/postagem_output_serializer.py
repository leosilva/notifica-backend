from rest_framework import serializers

from apps.accounts.serializers import UsuarioSerializer


class PostagemOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    titulo = serializers.CharField()
    corpo = serializers.CharField()
    gradiente_fundo = serializers.CharField(required=False, allow_null=True)
    imagem = serializers.URLField(required=False, allow_null=True)
    publicado_em = serializers.DateTimeField(required=False)
    disponivel = serializers.BooleanField()
    usuario = UsuarioSerializer(required=False)
