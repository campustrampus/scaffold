# pylint: disable=duplicate-code
"""
Testing CRUD operations on /api/foo* endpoints
"""
import json

import pytest

from app import Foo

# noinspection PyUnresolvedReferences
from tests.fixtures import *
from tests.utils import assert_attribute_in_collection, \
    assert_id_in_relationships

BASE_URI = '/api/v1/foos'

pytestmark = pytest.mark.usefixtures('legacy_database_seed')


@pytest.mark.unittest
def test_read_foo_collection(client, auth_headers):
    """
    Read Customer Collection
    """
    endpoint = BASE_URI
    resp = client.get(
        endpoint,
        headers=auth_headers,
    )
    data = json.loads(resp.data)
    assert resp.status_code == 200
    assert data['meta']['count'] == 1
    assert assert_attribute_in_collection(data, 'name', 'Bar')


@pytest.mark.unittest
def test_create_foo(client, auth_headers):
    """
    Create Customer
    """
    data_input = {
        "data": {
            "type": "Foo",
            "attributes": {
                "name": "EvilFoo",
            }
        }
    }
    endpoint = BASE_URI
    resp = client.post(
        endpoint,
        headers=auth_headers,
        json=data_input,
    )
    data_output = json.loads(resp.data)
    assert resp.status_code == 201
    for attr_name, attr_value in data_input['data']['attributes'].items():
        assert data_output['data']['attributes'][attr_name] == attr_value


@pytest.mark.unittest
def test_update_foo(client, auth_headers):
    """
    Update Customer
    """
    endpoint = BASE_URI
    resp = client.get(
        endpoint,
        headers=auth_headers,
    )

    data = json.loads(resp.data)
    assert resp.status_code == 200
    foo_id = data['data'][0]['id']

    data_input = {
        "data": {
            "type": "Foo",
            "id": foo_id,
            "attributes": {
                "name": "EvilerFoo",
            }
        }
    }
    endpoint = BASE_URI + '/' + foo_id
    resp = client.patch(
        endpoint,
        headers=auth_headers,
        json=data_input,
    )
    assert resp.status_code == 200
    resp = client.get(
        endpoint,
        headers=auth_headers,
    )
    data_output = json.loads(resp.data)
    assert resp.status_code == 200
    for attr_name, attr_value in data_input['data']['attributes'].items():
        assert data_output['data']['attributes'][attr_name] == attr_value


@pytest.mark.unittest
def test_delete_foo(client, auth_headers):
    """
    Delete Customer
    """
    endpoint = BASE_URI

    resp = client.get(
        endpoint,
        headers=auth_headers,
    )
    data = json.loads(resp.data)
    foo_id = data['data'][0]['id']
    resp = client.delete(endpoint + f'/{foo_id}', headers=auth_headers)
    assert resp.status_code == 204
