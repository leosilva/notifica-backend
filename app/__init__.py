import os

import cloudinary
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from app.settings import Settings

_ = load_dotenv()

app = Flask(__name__)
app.config.from_object(Settings)

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

app.config.update(
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=False,
    SESSION_COOKIE_HTTPONLY=True,
)

api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
oauth = OAuth(app)

CORS(
    app,
    supports_credentials=True,
    origins=[
        os.getenv('FRONTEND_BASE_URL', 'http://localhost:5173'),
        'http://localhost:5173',
        'http://127.0.0.1:5173',
        'http://0.0.0.0:5173'
    ],
    allow_headers=['Content-Type', 'Authorization', 'X-CSRF-Token'],
)

from app.auth.models import Usuario


@jwt.user_lookup_loader
def user_lookup(_jwt_header, jwt_data):
    return Usuario.query.get(jwt_data['sub'])


oauth.register(
    name='suap',
    client_id=os.getenv('SUAP_CLIENT_ID'),
    client_secret=os.getenv('SUAP_CLIENT_SECRET'),
    authorize_url='https://suap.ifrn.edu.br/o/authorize/',
    access_token_url="https://suap.ifrn.edu.br/o/token/",
    api_base_url="https://suap.ifrn.edu.br/api/",
)

cloudinary.config(secure=True)

from app.auth import auth_bp
from app.carrossel import carrossel_bp
from app.noticias import noticias_bp
from app.postagens import postagens_bp

api.register_blueprint(auth_bp)
api.register_blueprint(postagens_bp)
api.register_blueprint(noticias_bp)
api.register_blueprint(carrossel_bp)

from . import routes
