"""
    Initializer for Scaffold flask app.
"""

import base64
import binascii

from logging.config import dictConfig

from flask import Flask
from flask_admin import Admin
from flask_healthz import healthz

from app.api import api_bp
from app.api.admin import AuthAdminIndexView
from app.api.models import *
from app.api.schema import create_api
from app.api.seed_test_db import init_sql_db
from app.commands import register_commands
from app.config import DevelopmentConfig, TestingConfig, ProductionConfig, \
    MigrateConfig
from app.extensions import db, bootstrap, login_manager, migrate
from app.tasks import celery
from app.errors import AuthError, handle_generic_error, BadRequestError

config_map = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'migrate': MigrateConfig,
}


if os.getenv('DD_TRACE_ENABLED') and os.getenv('DD_TRACE_ENABLED').lower() != 'false':
    # pylint: disable=line-too-long
    ddtrace.patch_all(Logs=True)
    LOG_FORMAT = """%(asctime)s - [%(levelname)s] | %(funcName)s:%(lineno)d | %(message)s [dd.service=%(dd.service)s dd.env=%(dd.env)s dd.version=%(dd.version)s dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s]"""
else:
    LOG_FORMAT = """%(asctime)s - [%(levelname)s] | %(funcName)s:%(lineno)d | %(message)s"""


dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': LOG_FORMAT
        }
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})




# Turn on/off with boolean in config; defaults to True for Dev
def seed_db(app):
    """ Initialize a temporary database
    :param app: A Flask() object
    """
    with app.app_context():
        init_sql_db(True)


def create_app() -> Flask:
    """Helper factory function for the app
    :return: Flask()
    """
    return factory()


def create_celery():
    """Helper factory function for celery
    :return: Celery()
    """
    return factory(mode='celery')


# pylint: disable=no-member
def factory(mode='app'):
    """
        App factory method.
    """

    # log_format = ""
    app = Flask(__name__)

    config = config_map.get(app.config['ENV'], DevelopmentConfig)
    app.config.from_object(config)
    app.register_blueprint(api_bp)

    configure_celery(app)

    @app.shell_context_processor
    # pylint: disable=unused-variable
    def shell_context():
        return {
            'db': db,
            'User': User,
        }

    initialize_extensions(app)
    initialize_admin(app)
    initialize_login_manager()
    register_commands(app)
    register_error_handlers(app)
    configure_health_checks(app)

    seed = app.config['SEED_DB']
    if seed:
        seed_db(app)

    if mode == 'app':
        return app
    if mode == 'celery':
        return celery


def initialize_admin(app):
    """ Initialize our admin portal
    :param app: A Flask() object
    """
    admin = Admin(
        app,
        name='Scaffold admin console',
        template_mode='bootstrap3',
        index_view=AuthAdminIndexView(),
        base_template='custom_master.html',
    )
    register_admin_views(admin)


def register_error_handlers(app):
    """
    Registers errors within the app so they are returned as formatted
    :param app: The Flask application where the errors are registered.
    :return: N/A
    """
    app.register_error_handler(BadRequestError, handle_generic_error)
    app.register_error_handler(400, handle_generic_error)
    app.register_error_handler(AuthError, handle_generic_error)
    app.register_error_handler(403, handle_generic_error)


def initialize_extensions(app):
    """ Initialize the app extensions
     :param app: A Flask() object
     """
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        create_api(app)


def configure_health_checks(app):
    """
    Initialize a health check endpoint for kubernetes
    :param app: A Flask() object
    """
    app.register_blueprint(healthz, url_prefix='/healthz')
    app.config['HEALTHZ'] = {'liveness': 'app.api.healthz.liveness'}


def initialize_login_manager():
    """ Initialize our login manger
    :param app: A Flask() object
    :return: None
    """
    @login_manager.request_loader
    def load_user_from_header(request):
        user = load_token_user(request)


# pylint: disable=unused-variable
def load_token_user(request):
    """
    Loads the user for a given request from the request args or header.
    :param request: The incoming API request.
    :return: A sqlAlchemy User object.
    """
    # pylint: disable=import-outside-toplevel
    result = None
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return result
    encoded_token = auth_header.replace('Basic ', '', 1)
    try:
        token = base64.b64decode(encoded_token).decode()
    # If the key is not in the correct format, pass back None
    except (binascii.Error, UnicodeDecodeError) as error:
        raise AuthError(
            'Invalid Authorization token. Was the token base64 encoded?',
            401) from error
    cleaned_token = token.strip()
    key_hash = get_hash(cleaned_token)
    user = User.query.filter_by(token=key_hash).first()
    if user:
        result = user
    else:
        raise AuthError('Invalid Authorization token', 401)
    return result


def configure_celery(app):
    """ Configure and initialize celery
    :param app: A Flask() object
    """
    celery.conf.update(
        broker_url=app.config['CELERY_BROKER_URL'],
        result_backend=app.config['CELERY_RESULT_BACKEND'],
    )

    # pylint: disable=too-few-public-methods
    class ContextTask(celery.Task):
        """ Give our celery instance context to the app
        """
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    celery.finalize()
