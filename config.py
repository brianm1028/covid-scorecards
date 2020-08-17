from os import environ, path

class Permissions:
    SUPERUSER = 512
    SNAPSHOT_ADMIN = 256
    PPE_ADMIN = 128
    SPACE_ADMIN = 64
    STAFF_ADMIN = 32
    TRANS_ADMIN = 16
    PPE_MAINTAIN = 8
    SPACE_MAINTAIN = 4
    STAFF_MAINTAIN = 2
    TRANS_MAINTAIN = 1

    DISTRICT = 1024
    FACILITY = 2048

    @staticmethod
    def lookup(permset):
        perms = {
            1: Permissions.TRANS_MAINTAIN,
            2: Permissions.STAFF_MAINTAIN,
            4: Permissions.SPACE_MAINTAIN,
            8: Permissions.PPE_MAINTAIN,
            16: Permissions.TRANS_ADMIN,
            32: Permissions.STAFF_ADMIN,
            64: Permissions.SPACE_ADMIN,
            128: Permissions.PPE_ADMIN,
            256: Permissions.DISTRICT_ADMIN,
            512: Permissions.SUPERUSER
        }
        return [perms[p] for p in perms.keys() if Permissions.check(perms[p],permset)]

    @staticmethod
    def check(perm, permset):
        return (perm == (perm & permset))


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
