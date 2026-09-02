import enum

import marshmallow as ma

from app.auth.schema import UsuarioSchema
from app.postagens.models import Visibilidade


class Tipo(enum.Enum):
    POSTAGEM = 'postagem'
    NOTICIA = 'noticia'


class ConteudoSchema(ma.Schema):
    id = ma.fields.Integer(required=True)
    titulo = ma.fields.String(required=True)
    corpo = ma.fields.String(required=True)
    url = ma.fields.URL(allow_none=True)
    imagem = ma.fields.URL()
    gradiente = ma.fields.String(allow_none=True)
    visibilidade = ma.fields.Enum(Visibilidade, by_value=True)
    autor = ma.fields.Nested(UsuarioSchema)
    tipo = ma.fields.Enum(Tipo, by_value=True)


class SetorConteudoSchema(ma.Schema):
    setor = ma.fields.String(required=True)
