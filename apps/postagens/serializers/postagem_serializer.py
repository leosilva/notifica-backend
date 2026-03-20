from rest_framework import serializers
from apps.accounts.models import Usuario
from apps.accounts.serializers import UsuarioSerializer

class PostagemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    corpo = serializers.CharField()
    usuario = serializers.SerializerMethodField()


    def get_usuario(self, postagem):
        user = Usuario.objects.get(pk=postagem.usuario_id)
        return UsuarioSerializer(user).data
