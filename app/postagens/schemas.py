import marshmallow as ma
from flask_smorest.fields import Upload
from marshmallow import validate

from app.auth.schema import UsuarioSchema
from app.postagens.models import Estado, Visibilidade


class PostagemPostSchema(ma.Schema):
    titulo = ma.fields.String(required=True, validate=validate.Length(max=128))
    corpo = ma.fields.String(required=True, validate=validate.Length(max=324))
    imagem = ma.fields.Raw(metadata={"type": "string", "format": "binary"})
    gradiente = ma.fields.String(validate=validate.Length(max=64))
    visibilidade = ma.fields.Enum(Visibilidade, by_value=True)


class PostagemSchema(ma.Schema):
    id = ma.fields.Integer()
    titulo = ma.fields.String(required=True, validate=validate.Length(max=128))
    corpo = ma.fields.String(required=True, validate=validate.Length(max=324))
    gradiente = ma.fields.String(validate=validate.Length(max=500))
    visibilidade = ma.fields.Enum(Visibilidade, by_value=True)
    estado = ma.fields.Enum(Estado, by_value=True)
    autor = ma.fields.Nested(UsuarioSchema)


class PostagemQuerySchema(ma.Schema):
    estado = ma.fields.Enum(Estado, by_value=True)
    visibilidade = ma.fields.Enum(Visibilidade, by_value=True)


class PostagemReviewSchema(ma.Schema):
    estado = ma.fields.Enum(
        Estado,
        by_value=True,
        validate=validate.OneOf(
            [Estado.REVISAO, Estado.NEGADA]
        )
    )
