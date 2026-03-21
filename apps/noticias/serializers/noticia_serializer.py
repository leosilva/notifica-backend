from django.core.files.images import ImageFile
from django.core.exceptions import ValidationError
from rest_framework import serializers
from apps.accounts.serializers import UsuarioSerializer
from apps.noticias.services import upload_image
from apps.noticias.models import Noticia


class ImageFileOuString(serializers.Field):
    def to_internal_value(self, data):
        if isinstance(data, ImageFile):
            return upload_image(data).url
        if isinstance(data, str):
            return data
        raise ValidationError('Deve ser um ImageFile ou String.')


    def to_representation(self, value) -> str:
        return str(value)


class NoticiaSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    titulo = serializers.CharField()
    sumario = serializers.CharField()
    link = serializers.URLField()
    imagem = ImageFileOuString(required=False)
    publicado_em = serializers.DateField(required=False)
    usuario = UsuarioSerializer(required=False)


    def create(self, validated_data):
        return Noticia.objects.create(**validated_data)
