from flask_smorest import Blueprint

noticias_bp = Blueprint(
    'noticias',
    import_name='noticias',
    url_prefix='/noticias/'
)

from . import models, routes
