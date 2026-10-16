from app.carrossel import carrossel_bp
from app.carrossel.schemas import ConteudoSchema
from app.carrossel.utils import get_conteudo


@carrossel_bp.route('/')
@carrossel_bp.response(200, schema=ConteudoSchema(many=True))
def carrossel():
    return get_conteudo()
