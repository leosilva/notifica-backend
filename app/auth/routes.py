from flask import jsonify, redirect, url_for
from flask_jwt_extended import (
    create_access_token,
    current_user,
    jwt_required,
    unset_jwt_cookies,
)
from flask_jwt_extended.utils import set_access_cookies
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
        }, 500

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
            matricula=user_data['matricula'],
        )
        db.session.add(usuario)

    usuario.nome = user_data['nome']
    usuario.email = user_data['email']
    usuario.role = user_data['role']

    db.session.commit()

    return utils.authenticate_user(usuario)


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    response = redirect(utils.BASE_FRONTEND_URL)

    set_access_cookies(
        response, create_access_token(
            identity=str(current_user.id)
        )
    )

    return response


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
@auth_bp.response(200)
def logout():
    res = jsonify({
        'msg': 'logout concluído.'
    })
    unset_jwt_cookies(res)
    return res
