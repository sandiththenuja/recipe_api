class Config:
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://sandith:welegoda@localhost:8000/smilecook'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'secret-key'
    JWT_ERROR_MESSAGE_KEY = 'message'

    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']