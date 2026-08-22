import os

from dotenv import load_dotenv

_ = load_dotenv()

class Settings:
    SECRET_KEY = os.getenv('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

    API_TITLE = 'notIFica'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.2'

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_TOKEN_LOCATION = ['headers', 'cookies']
