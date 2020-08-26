from os import environ, path

class Config:
    """Set Flask configuration from environment variables."""

    # General Config
    FLASK_APP = 'wsgi.py'
    FLASK_ENV = environ.get('FLASK_ENV')
    #AWS_ACCESS_KEY = environ.get('AWS_ACCESS_KEY')
    #AWS_SECRET_KEY = environ.get('AWS_SECRET_KEY')
    DEBUG = True
    SECRET_KEY = 'Apr5813213455894433!'

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask Caching
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300

    # Flask-Session
    SESSION_TYPE = 'filesystem'
    #SESSION_REDIS = 'redis://covidmetrics-redis.zlpdik.0001.use1.cache.amazonaws.com:6379'