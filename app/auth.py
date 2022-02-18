"""
A module for handling API request authorization and authentication.
"""
import hashlib
from jose import jwt

SALT = "98a73a901730a927671957b5e9991f455cf703c21a3cabab2f3d95b25c405645"


def get_hash(text):
    """
    Returns a secure hash value for the given text.
    :param text: Any basic string.
    :return: A hex representation of the hash.
    """
    return hashlib.sha256(SALT.encode() + text.encode()).hexdigest()


def require_scope(scope, token):
    """
    Determines if a token has the required scopes (permissions).
    :param scope: A string representation of a scope eg: read:stations
    :param token: A trusted JWT access token that contains scopes
    :return: A boolean that indicates whether or not the scope is allowed by the token
    """
    unverified_claims = jwt.get_unverified_claims(token)
    if unverified_claims.get("scope"):
        token_scopes = unverified_claims["scope"].split()
        for token_scope in token_scopes:
            if token_scope == scope:
                return True
    return False
