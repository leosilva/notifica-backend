from datetime import timedelta

from flask_jwt_extended import create_access_token, create_refresh_token
from requests.exceptions import HTTPError
from sqlalchemy import select
from werkzeug.security import generate_password_hash

from app import db
from app.auth import auth_bp, utils
from app.auth.models import Usuario
from app.auth.schemas import UsuarioPostSchema


@auth_bp.route('/users/register', methods=['POST'])
@auth_bp.arguments(UsuarioPostSchema, location="json")
def register_user(data):
    if db.session.scalar(
        select(Usuario).where(Usuario.matricula == data['matricula'])
    ):
        return {
            'erro': 'Usuário com essa matrícula já existe. Tente fazer login.'
        }, 409

    try:
        token = utils.get_suap_token(data)
    except HTTPError:
        return {
            'erro': 'Credenciais inválidas.'
        }, 400

    user_data = utils.get_user_data(token)

    if user_data.get('campus') != 'CM':
        return {
            'erro': 'Campus não autorizado'
        }, 403

    usuario = Usuario(
        nome=user_data['nome'],
        matricula=data['matricula'],
        email=user_data['email'],
        senha=generate_password_hash(data['senha']),
        role=user_data['role'],
    )
    db.session.add(usuario)
    db.session.commit()

    return {
        'access': create_access_token(
            identity=usuario.id,
            expires_delta=timedelta(minutes=5)
        ),
        'refresh': create_refresh_token(
            identity=usuario.id,
            expires_delta=timedelta(days=7)
        )
    }, 201
