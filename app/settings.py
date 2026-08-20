import os
import secrets

from dotenv import load_dotenv

_ = load_dotenv()

class Settings:
    SECRET_KEY = secrets.token_hex(16)

    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

    API_TITLE = 'notIFica'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.2'

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
