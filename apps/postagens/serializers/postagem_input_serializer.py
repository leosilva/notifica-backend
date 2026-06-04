from rest_framework import serializers


class PostagemInputSerializer(serializers.Serializer):
    titulo = serializers.CharField()
    corpo = serializers.CharField()
    disponivel = serializers.BooleanField(required=False)
