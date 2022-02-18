"""
Defines classes and methods used for app error handling.
"""


from flask import jsonify


class AuthError(Exception):
    """
    Error raised specifically for authentication/authorization issues
    """
    def __init__(self, detail, status_code):
        self.title = 'AUTH_ERROR'
        self.detail = detail
        self.status_code = status_code
        super().__init__()


class BadRequestError(Exception):
    """
    Error raised specifically for bad request issues
    """
    def __init__(self, detail, status_code):
        self.title = 'BAD_REQUEST'
        self.detail = detail
        self.status_code = status_code
        super().__init__()


def get_scope_insufficient_error_message(scope, username):
    """
    Returns a generic error message for users who don't have proper permissions.
    :param scope: A JWT OAuth permission scope in string form eg: read:stations
    :param username: The name of the user trying to perform the action
    :return: An error message string.
    """
    return f'{username} does not have permission to do this action. Required scope {scope}'


def handle_generic_error(exception):
    """
    Handles the formatting of bad request errors
    :param exception: The actual bad request exception
    :return: A JSON string representing the error
    """
    response = jsonify(detail=exception.detail, title=exception.title)
    response.status_code = exception.status_code
    return response
