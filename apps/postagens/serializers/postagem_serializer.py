from rest_framework import serializers
from apps.accounts.models import Usuario
from apps.accounts.serializers import UsuarioSerializer
from apps.postagens.models import Postagem


class PostagemSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    corpo = serializers.CharField()
    publicado_em = serializers.DateTimeField(required=False)
    usuario = serializers.SerializerMethodField(required=False)


    def get_usuario(self, postagem):
        user = Usuario.objects.get(pk=postagem.usuario_id)
        return UsuarioSerializer(user).data


    def create(self, validated_data):
        return Postagem.objects.create(**validated_data)
