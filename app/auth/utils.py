from datetime import timedelta

from flask import redirect
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
)

BASE_SUAP_API_URL = 'https://suap.ifrn.edu.br/api'
BASE_FRONTEND_URL = 'http://localhost:5179'


def get_user_data(data: str) -> dict[str, str]:
    return {
        'matricula': data.get('identificacao'),
        'nome': data.get('nome_social') or data.get('nome_registro'),
        'email': data.get('email_google_classroom'),
        'campus': data.get('campus'),
        'role': data.get('tipo_usuario').upper(),
    }


def authenticate_user(usuario):
    response = redirect(BASE_FRONTEND_URL)

    set_access_cookies(response, create_access_token(
        identity=str(usuario.id), expires_delta=timedelta(minutes=5)
    ))

    set_refresh_cookies(response, create_refresh_token(
        identity=str(usuario.id), expires_delta=timedelta(days=7)
    ))

    return response
