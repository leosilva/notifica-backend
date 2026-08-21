from flask_smorest import Blueprint

postagens_bp = Blueprint(
    'postagens',
    import_name='postagens',
    url_prefix='/postagens/'
)

from app.postagens import models, routes
