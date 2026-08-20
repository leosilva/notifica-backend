from flask import Blueprint

auth_bp = Blueprint(
    'auth',
    import_name='auth',
    url_prefix='/api/v2/'
)

from . import models
