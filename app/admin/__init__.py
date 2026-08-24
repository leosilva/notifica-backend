from flask_smorest import Blueprint

admin_bp = Blueprint(
    'admin',
    import_name='admin',
    url_prefix='/admin/'
)

from . import routes
