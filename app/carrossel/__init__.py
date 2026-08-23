from flask_smorest import Blueprint

carrossel_bp = Blueprint(
    'carrossel',
    import_name='carrossel',
    url_prefix='/carrossel/'
)

from . import routes
