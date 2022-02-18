""" Utility functions for unit and integration tests
"""
import os
import requests


def get_token():
    """ Get integration token from env
    """
    return os.getenv('INTEGRATION_TOKEN', 'not a real token')


def get_session():
    """ Create requests session for testing
    """
    token = get_token()
    headers = {
        "Content-Type": "application/vnd.api+json",
        "Accept": "application/vnd.api+json",
        "Authorization": f'Basic {token}'
    }

    session = requests.Session()
    session.headers.update(headers)

    return session


def assert_attribute_in_collection(data, attr, value):
    """ Helper function to check if an attribute is present in a collection
    """
    for relationship_data in data['data']:
        if relationship_data['attributes'][attr] == value:
            return True
    return False


def assert_id_in_relationships(data, value):
    """ Helper function to check if an relationship ID is present
    """
    for relationship_data in data['data']:
        if relationship_data['id'] == value:
            return True
    return False
