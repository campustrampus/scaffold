""" Utility functions
"""
from datetime import datetime
from functools import wraps

from flask import request, current_app
from flask_login import current_user


def get_sanitized_headers(headers):
    """ A helper function to remove sensitive headers
    :param headers: The request headers
    :type headers: EnvironHeaders
    """
    sanitized_headers = dict(headers)
    if 'Cookie' in sanitized_headers:
        del sanitized_headers['Cookie']
    if 'Authorization' in sanitized_headers:
        del sanitized_headers['Authorization']
    return sanitized_headers


def audit_logging(func):
    """ A decorator that logs audit information for requests
    :param func: The view function to decorate.
    :type func: function
    """
    @wraps(func)
    def audit_decorator(*args, **kwargs):
        now = datetime.utcnow()
        time = now.strftime('%Y-%m-%d %H:%M:%S')

        username = "Anonymous"
        if current_user.is_authenticated:
            username = current_user.username

        audit_info = {
            "user": username,
            "time": time,
            "method": request.method,
            "base_url": request.base_url,
            "params": request.args,
        }

        sanitized_headers = get_sanitized_headers(request.headers)

        audit_info_verbose = {
            "headers": sanitized_headers,
            "full_url": request.full_path,
        }

        if request.method in ['POST', 'PATCH'] and request.is_json:
            audit_info.update({"data": request.json})
            audit_info_verbose.update({"data": request.data})

        audit_log = f"Audit: {audit_info}"
        audit_log_verbose = f"Audit: {audit_info_verbose}"

        current_app.logger.info(audit_log)
        current_app.logger.debug(audit_log_verbose)

        return func(*args, **kwargs)

    return audit_decorator
