""" tests test_factory

Test our factory methods
"""
import pytest


@pytest.mark.unittest
def test_create_app(app):
    """ Test create_app
    """
    assert not app.config['DEBUG']
    assert app.config['TESTING']
