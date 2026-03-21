from rest_framework import serializers


class UsuarioSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    nome = serializers.SerializerMethodField()
    email = serializers.EmailField()


    def get_nome(self, usuario) -> str:
        return f'{usuario.nome} {usuario.sobrenome}'
