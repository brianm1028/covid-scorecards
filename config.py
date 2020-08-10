from os import environ, path


class Config:
    """Set Flask configuration from environment variables."""

    # General Config
    FLASK_APP = 'wsgi.py'
    FLASK_ENV = environ.get('FLASK_ENV')
    #AWS_ACCESS_KEY = environ.get('AWS_ACCESS_KEY')
    #AWS_SECRET_KEY = environ.get('AWS_SECRET_KEY')
    DEBUG = True

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask Caching
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300