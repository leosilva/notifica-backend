import os

from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy

from app.settings import Settings

_ = load_dotenv()

app = Flask(__name__)
app.config.from_object(Settings)

api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
oauth = OAuth(app)

oauth.register(
    name='suap',
    client_id=os.getenv('SUAP_CLIENT_ID'),
    client_secret=os.getenv('SUAP_CLIENT_SECRET'),
    authorize_url='https://suap.ifrn.edu.br/o/authorize/',
    access_token_url="https://suap.ifrn.edu.br/o/token/",
    api_base_url="https://suap.ifrn.edu.br/api/",
)

from app.auth import auth_bp
from app.postagens import postagens_bp

api.register_blueprint(auth_bp)
api.register_blueprint(postagens_bp)

from . import routes
