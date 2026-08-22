from app.noticias import noticias_bp


@noticias_bp.route('/')
def index():
    return 'hello, world!'
