from flask_smorest import Blueprint

auth_bp = Blueprint(
    'auth',
    import_name='auth',
    url_prefix='/auth/'
)

from . import models, routes
