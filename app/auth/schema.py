from datetime import datetime

import marshmallow as ma
from marshmallow import validate

from app.auth.models import Role


class UsuarioSchema(ma.Schema):
    id = ma.fields.Integer()
    nome = ma.fields.String()
    matricula = ma.fields.String(validate=lambda m: m.isnumeric())
    email = ma.fields.Email()
    role = ma.fields.Enum(Role, by_value=True)
    criado_em = ma.fields.DateTime(validate=lambda ce: ce < datetime.now())
    atualizado_em = ma.fields.DateTime(validate=lambda ce: ce < datetime.now())
