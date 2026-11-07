import os

class Config:
    DEBUG = False

    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://sandith:welegoda@localhost:8000/smilecook'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SECRET_KEY = 'secret-key'
    JWT_ERROR_MESSAGE_KEY = 'message'

    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    UPLOADED_IMAGES_DEST = 'static/images'  # attribute name in extensions.py 
    # image_set = UploadSet('images', IMAGES)

    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 10 * 60  # 10 mins 

    RATELIMIT_HEADERS_ENABLED = True

class DevelopmentConfig(Config):
    DEBUG = True
    
    SECRET_KEY = 'secret-key'

    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://sandith:welegoda@localhost:8000/smilecook'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class ProductionConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class StagingConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
