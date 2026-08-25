import os
from datetime import timedelta
from typing import final

from dotenv import load_dotenv

_ = load_dotenv()

def get_database_uri():
    user     = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD')
    host     = os.getenv('DB_HOST', 'localhost')
    port     = os.getenv('DB_PORT', '3306')
    database = os.getenv('DB_NAME', 'notifica')

    return f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'


@final
class Settings:
    SECRET_KEY = os.getenv('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = get_database_uri()

    API_TITLE = 'notIFica'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.2'
    OPENAPI_URL_PREFIX = '/docs'
    OPENAPI_SWAGGER_UI_PATH = '/'
    OPENAPI_SWAGGER_UI_URL = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist@3.25.0/'

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_TOKEN_LOCATION = ['headers', 'cookies']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
