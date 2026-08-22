import marshmallow as ma
from marshmallow import validate

from app.auth.schema import UsuarioSchema
from app.noticias.models import Fonte, Visibilidade


class NoticiaPostSchema(ma.Schema):
    titulo = ma.fields.String(required=True, validate=validate.Length(max=255))
    corpo = ma.fields.String(required=True)
    url = ma.fields.URL()
    visibilidade = ma.fields.Enum(Visibilidade, by_value=True)


class NoticiaImagemSchema(ma.Schema):
    imagem = ma.fields.Raw(metadata={"type": "string", "format": "binary"})


class NoticiaSchema(ma.Schema):
    id = ma.fields.Integer()
    titulo = ma.fields.String(required=True, validate=validate.Length(max=255))
    corpo = ma.fields.String(required=True)
    url = ma.fields.URL()
    imagem = ma.fields.URL()
    fonte = ma.fields.Enum(Fonte, by_value=True)
    autor = ma.fields.Nested(UsuarioSchema)
    visibilidade = ma.fields.Enum(Visibilidade, by_value=True)
    criado_em = ma.fields.DateTime()
    atualizado_em = ma.fields.DateTime()


class NoticiaQuerySchema(ma.Schema):
    visibilidade = ma.fields.Enum(Visibilidade, by_value=True)
