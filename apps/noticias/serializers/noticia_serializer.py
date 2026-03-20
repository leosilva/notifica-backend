from django.core.files.images import ImageFile
from django.core.exceptions import ValidationError
from rest_framework import serializers
from apps.accounts.serializers import UsuarioSerializer
from apps.noticias.models import Noticia
from apps.noticias.services import upload_image


class ImageFileOuString(serializers.Field):
    def to_internal_value(self, data):
        if isinstance(data, ImageFile):
            return upload_image(data).url
        if isinstance(data, str):
            return data
        raise ValidationError('Deve ser um ImageFile ou String.')


class NoticiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noticia
        fields = ['titulo', 'sumario', 'link', 'imagem', 'data', 'usuario']

    imagem = ImageFileOuString()
    usuario = UsuarioSerializer(read_only=True, required=False)
