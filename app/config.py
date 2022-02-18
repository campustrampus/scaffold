""" app config

Configuration objects
"""
# pylint: disable=too-few-public-methods
import os


def get_seed_db():
    """
    Helper function to process FLASK_SEED_DB environment variable
    :return: bool
    """
    result = False
    seed_db = os.getenv('FLASK_SEED_DB', 'false')
    if seed_db.lower() != 'false':
        result = True
    return result


class Config():
    """ Base Config object
    """
    DEBUG = False
    TESTING = False
    SEED_DB = get_seed_db()
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'super_secret_key')
    DISK_WRITE_BASE_PATH = os.getenv('DISK_WRITE_BASE_PATH', '/tmp')

    # Flask-Sqlalchemy Settings
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite://')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Auth0 Settings
    #AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID', '')
    #AUTH0_AUDIENCE = os.getenv('AUTH0_AUDIENCE', 'https://test')
    #AUTH0_SCOPE = os.getenv('AUTH0_SCOPES', "openid profile email read")
    #AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET', 'api_secret_key')
    #AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN', 'test.auth0.com')
    #AUTH0_LOGOUT_URL = os.getenv('AUTH0_LOGOUT_URL', 'http://localhost:8081/')
    #AUTH0_CALLBACK_URL = os.getenv('AUTH0_CALLBACK_URL', 'http://localhost:8081/admin/callback')

    # Celery Settings
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', '')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', '')


    # Flask-Admin Settings
    FLASK_ADMIN_SWATCH = 'darkly'
    ADMIN_URL_SCHEME = os.getenv('ADMIN_URL_SCHEME', 'https')

    # SAFRS Settings
    MAX_PAGE_LIMIT = 2500
    SWAGGER_BASE_URL = os.getenv('SWAGGER_BASE_URL', 'localhost:8081')


class DevelopmentConfig(Config):
    """ Development Config Object
    """
    DEBUG = True


class MigrateConfig(Config):
    """ Migrate Config Object
    """
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI', 'postgresql://admin:admin@localhost:5432')


class TestingConfig(Config):
    """ Testing Config Object
    """
    TESTING = True
    SEED_DB = False

    # Celery Settings
    CELERY_BROKER_URL = 'memory://'
    CELERY_RESULT_BACKEND = 'rpc://'


class ProductionConfig(Config):
    """ Production Config Object
    """
    SEED_DB = False
