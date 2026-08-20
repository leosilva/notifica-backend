from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy

from app.settings import Settings

app = Flask(__name__)
app.config.from_object(Settings)

api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

from app.auth import auth_bp

api.register_blueprint(auth_bp)

from . import routes
