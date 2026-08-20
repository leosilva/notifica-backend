import requests

BASE_SUAP_API_URL = 'https://suap.ifrn.edu.br/api'


def get_suap_token(data: dict[str, str]) -> str:
    res = requests.post(f'{BASE_SUAP_API_URL}/token/pair', json={
        'username': data['matricula'],
        'password': data['senha'],
    })
    print(res.status_code)
    res.raise_for_status()
    return res.json()['access']


def get_user_data(token: str) -> dict[str, str]:
    res = requests.get(f'{BASE_SUAP_API_URL}/rh/eu/', headers={
        'Authorization': f'Bearer {token}'
    })
    body = res.json()

    return {
        'nome': body.get('nome_social') or body.get('nome_registro'),
        'email': body.get('email_google_classroom'),
        'campus': body.get('campus'),
        'role': body.get('tipo_usuario').upper(),
    }
