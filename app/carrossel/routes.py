from app.carrossel import carrossel_bp
from app.carrossel.schemas import ConteudoSchema, SetorConteudoSchema
from app.carrossel.utils import get_conteudo


@carrossel_bp.route('/')
@carrossel_bp.arguments(SetorConteudoSchema, location='query')
@carrossel_bp.response(200, schema=ConteudoSchema(many=True))
def carrossel(query):
    return get_conteudo(query.get('setor'))
