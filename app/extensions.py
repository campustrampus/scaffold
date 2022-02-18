""" app extensions
Third party extensions
"""
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
migrate = Migrate(compare_type=True)
