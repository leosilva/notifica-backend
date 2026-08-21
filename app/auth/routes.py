from flask import url_for
from sqlalchemy import select

from app import db, oauth
from app.auth import auth_bp, utils
from app.auth.models import Usuario


@auth_bp.route('/suap/login')
def suap_login():
    return oauth.suap.authorize_redirect(
        url_for(
            'auth.suap_callback',
            _external=True
        )
    )


@auth_bp.route("/suap/callback")
def suap_callback():
    _ = oauth.suap.authorize_access_token()

    res = oauth.suap.get('/api/rh/eu')
    if res.status_code != 200:
        return {
            'erro': 'Erro de requisição do SUAP.'
        }, 400

    user_data = utils.get_user_data(res.json())

    if user_data['campus'] != 'CM':
        return {
            'erro': 'Campus não autorizado.'
        }, 403

    usuario = db.session.scalar(
        select(Usuario).where(
            Usuario.matricula == user_data['matricula']
        )
    )

    if not usuario:
        usuario = Usuario(
            nome=user_data['nome'],
            matricula=user_data['matricula'],
            email=user_data['email'],
            role=user_data['role'],
        )
        db.session.add(usuario)
        db.session.commit()

    return utils.authenticate_user(usuario)
