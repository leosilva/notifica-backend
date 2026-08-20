import marshmallow as ma
from marshmallow.validate import Length


class UsuarioPostSchema(ma.Schema):
    matricula = ma.fields.Str(required=True)

    senha = ma.fields.Str(
        required=True,
        validate=Length(
            min=8,
            error='Senha não pode ser menor que 8 caracteres.'
        )
    )

    @ma.validates('matricula')
    def validate_matricula(self, value: str, **kwargs) -> None:
        if not value.isnumeric():
            raise ma.ValidationError('Matrícula deve ser inteiramente numérica.')
