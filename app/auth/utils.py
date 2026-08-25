from dotenv import load_dotenv

from app.auth.models import Role

_ = load_dotenv()

BASE_SUAP_API_URL = 'https://suap.ifrn.edu.br/api'


def get_user_data(data: dict) -> dict[str, str | Role | None]:
    return {
        'matricula': data.get('identificacao'),
        'nome': data.get('nome_social') or data.get('nome_registro'),
        'email': data.get('email_google_classroom'),
        'campus': data.get('campus'),
        'role': Role(data.get('tipo_usuario', '').lower()),
    }
