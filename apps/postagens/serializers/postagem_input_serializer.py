from django.core.files.base import File
from django.core.files.images import ImageFile
from django.core.files.uploadedfile import UploadedFile
from rest_framework import serializers

from apps.noticias.services import upload_image
from apps.postagens.models import Postagem


class ImageFileOuUrl(serializers.Field):
    def to_internal_value(self, data):
        if isinstance(data, (File, ImageFile, UploadedFile)):
            try:
                return upload_image(data).url
            except Exception as exc:
                raise serializers.ValidationError(
                    "Não foi possível enviar a imagem."
                ) from exc

        if isinstance(data, str):
            return serializers.URLField().run_validation(data)

        raise serializers.ValidationError(
            "Campo 'imagem' deve ser uma URL ou arquivo de imagem."
        )

    def to_representation(self, value) -> str:
        return str(value)


def validar_gradiente(valor: str) -> str:
    import re

    if not valor:
        raise serializers.ValidationError(
            "Campo 'gradiente_fundo' não pode estar vazio."
        )

    if not re.match(r'^linear-gradient\(', valor):
        raise serializers.ValidationError(
            "Campo 'gradiente_fundo' deve começar com 'linear-gradient('."
        )

    if not valor.endswith(')'):
        raise serializers.ValidationError(
            "Campo 'gradiente_fundo' deve terminar com ')'."
        )

    if not valor.count('(') == valor.count(')'):
        raise serializers.ValidationError(
            "Campo 'gradiente_fundo' contém parênteses desbalanceados."
        )

    proibido = {';', '{', '}', '<', '>', 'url('}
    if any(p in valor.lower() for p in proibido):
        raise serializers.ValidationError(
            "Campo 'gradiente_fundo' contém caracteres não permitidos."
        )

    return valor


class PostagemInputSerializer(serializers.Serializer):
    titulo = serializers.CharField()
    corpo = serializers.CharField()
    gradiente_fundo = serializers.CharField(
        required=False,
        allow_null=True,
        max_length=512,
        validators=[validar_gradiente],
    )
    imagem = ImageFileOuUrl(required=False, allow_null=True)
    disponivel = serializers.BooleanField(required=False)

    def validate(self, attrs):
        if attrs.get('gradiente_fundo') and attrs.get('imagem'):
            raise serializers.ValidationError(
                "Informe apenas 'gradiente_fundo' ou 'imagem', não ambos."
            )

        return attrs

    def create(self, validated_data):
        return Postagem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.titulo = validated_data.get('titulo', instance.titulo)
        instance.corpo = validated_data.get('corpo', instance.corpo)

        if 'gradiente_fundo' in validated_data:
            instance.gradiente_fundo = validated_data.get('gradiente_fundo')

            if instance.gradiente_fundo:
                instance.imagem = None

        if 'imagem' in validated_data:
            instance.imagem = validated_data.get('imagem')

            if instance.imagem:
                instance.gradiente_fundo = None

        instance.disponivel = validated_data.get('disponivel', instance.disponivel)
        instance.save()

        return instance
