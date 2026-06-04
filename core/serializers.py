from django.core.exceptions import ValidationError
from django.core.files.images import ImageFile
from rest_framework import serializers

from apps.accounts.serializers import UsuarioSerializer
from apps.noticias.models import Noticia
from apps.noticias.services import upload_image
from apps.postagens.models.postagem import Postagem


class ImageFileOuString(serializers.Field):
    def to_internal_value(self, data):
        if isinstance(data, ImageFile):
            return upload_image(data).url
        if isinstance(data, str):
            return data
        raise ValidationError("Campo 'imagem' deve ser um ImageFile ou String.")

    def to_representation(self, value) -> str:
        return str(value)


class ConteudoSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    titulo = serializers.CharField()
    corpo = serializers.CharField()
    link = serializers.URLField(required=False, allow_null=True, allow_blank=True)
    imagem = ImageFileOuString(required=False, allow_null=True)
    publicado_em = serializers.SerializerMethodField()
    disponivel = serializers.BooleanField()
    usuario = UsuarioSerializer(required=False)
    tipo = serializers.ChoiceField(choices=["postagem", "noticia"], write_only=True)

    def get_publicado_em(self, instance):
        publicado_em = getattr(instance, "publicado_em", None)

        if publicado_em is None:
            return None

        return publicado_em.isoformat()

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if isinstance(instance, Noticia):
            data["tipo"] = "noticia"
        elif isinstance(instance, Postagem):
            data["tipo"] = "postagem"

        return data

    def create(self, validated_data):
        tipo = validated_data.pop("tipo")

        if tipo == "noticia":
            validated_data["sumario"] = validated_data.pop("corpo")
            return Noticia.objects.create(**validated_data)
        elif tipo == "postagem":
            validated_data.pop("link", None)
            validated_data.pop("imagem", None)
            return Postagem.objects.create(**validated_data)
        else:
            raise ValueError("Tipo não identificado.")
