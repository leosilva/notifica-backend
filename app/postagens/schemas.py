import marshmallow as ma
from marshmallow import validate

from app.auth.schema import UsuarioSchema
from app.postagens.models import Estado, Visibilidade


class PostagemPostSchema(ma.Schema):
    titulo = ma.fields.String(required=True, validate=validate.Length(max=128))
    corpo = ma.fields.String(required=True, validate=validate.Length(max=324))
    imagem = ma.fields.Raw()
    gradiente = ma.fields.String(validate=validate.Length(max=500))
    visibilidade = ma.fields.Enum(Visibilidade, by_value=True)


    @ma.validates_schema
    def validate_background(self, data, **kwargs):
        if not ('imagem' in data or 'gradiente' in data):
            raise ma.ValidationError('Um campo de fundo deve ser passado.')

        if ('imagem' in data and 'gradiente' in data):
            raise ma.ValidationError('Apenas um campo de fundo deve ser passado.')


class PostagemSchema(ma.Schema):
    id = ma.fields.Integer()
    titulo = ma.fields.String(required=True, validate=validate.Length(max=128))
    corpo = ma.fields.String(required=True, validate=validate.Length(max=324))
    imagem = ma.fields.String()
    gradiente = ma.fields.String(validate=validate.Length(max=500))
    visibilidade = ma.fields.Enum(Visibilidade, by_value=True)
    estado = ma.fields.Enum(Estado, by_value=True)
    autor = ma.fields.Nested(UsuarioSchema)


class PostagemQuerySchema(ma.Schema):
    estado = ma.fields.Enum(Estado, by_value=True)
    visibilidade = ma.fields.Enum(Visibilidade, by_value=True)
