from json import load
import os
from dotenv import load_dotenv

load_dotenv()
user = os.getenv('DB_USER')
password = os.getenv('DB_PASS')
database = os.getenv('DB_TABLE')
test_database = os.getenv('TEST_DB')


class Config(object):
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY')

class ProductionConfig(Config):
    DEBUG = False
    ENV = 'PRODUCTION'

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{user}:{password}@localhost:5432/{database}'
    DEBUG = True
    ENV = 'DEVELOPMENT'
    MAIL_PORT = 1025
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    UPLOADED_PHOTOS_DEST = 'images'

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{user}:{password}@localhost:5432/{test_database}'
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True