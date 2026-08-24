from app.admin import admin_bp
from app.auth.models import Role
from app.auth.permissions import roles_required


@admin_bp.route('/')
@roles_required(Role.ADMIN)
def index():
    return 'hello, world!'
