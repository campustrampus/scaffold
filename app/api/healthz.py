"""
A module for health check functions for the application
"""
from flask_healthz import HealthError

from app.extensions import db


# pylint: disable=broad-except
def liveness():
    """
    A liveness check for the application
    """
    error_message = ''
    try:
        db.session.execute("SELECT 1")
    except Exception as db_error:
        error_message = f'{error_message}Unable to contact Database:{str(db_error)}\n'
    if error_message:
        raise HealthError(error_message)
