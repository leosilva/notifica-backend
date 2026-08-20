from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.settings import Settings

app = Flask(__name__)
app.config.from_object(Settings)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

from app.auth import auth_bp

app.register_blueprint(auth_bp)

from . import routes
