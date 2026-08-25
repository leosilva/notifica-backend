import os

from dotenv import load_dotenv
from flask import redirect
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
)

from app.auth.models import Role

_ = load_dotenv()

BASE_SUAP_API_URL = 'https://suap.ifrn.edu.br/api'
BASE_FRONTEND_URL = os.getenv('BASE_FRONTEND_URL', '')


def get_user_data(data: dict) -> dict[str, str | Role | None]:
    return {
        'matricula': data.get('identificacao'),
        'nome': data.get('nome_social') or data.get('nome_registro'),
        'email': data.get('email_google_classroom'),
        'campus': data.get('campus'),
        'role': Role(data.get('tipo_usuario', '').lower()),
    }
