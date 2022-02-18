"""
Test Source API routes
"""
import pytest


@pytest.mark.unittest
def test_index(client):
    """ Test the main index page
    """
    resp = client.get('/')
    print(resp.data)
    assert resp.status_code == 200
    assert b'Go to admin!' in resp.data


@pytest.mark.unittest
def test_admin_index(client):
    """ Test the admin index page
    """
    resp = client.get('/admin/')
    assert resp.status_code == 200


@pytest.mark.unittest
def test_admin_logout(client):
    """ Test the admin logout page
    """
    resp = client.get('/admin/logout')
    assert resp.status_code == 200
