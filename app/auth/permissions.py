from functools import wraps

from flask_jwt_extended import current_user
from flask_smorest import abort


def roles_required(*cargos_permitidos):
    def decorator(funcao):
        @wraps(funcao)
        def wrapper(*args, **kwargs):
            if current_user.role not in cargos_permitidos:
                abort(403)
            return funcao(*args, **kwargs)
        return wrapper
    return decorator
