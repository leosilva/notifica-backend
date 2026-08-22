from app import app


@app.route('/')
def index():
    return {
        'msg': 'a API está funcionando e pronta para uso.'
    }
