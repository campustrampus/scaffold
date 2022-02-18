"""
Testing for the authorization/authentication module.
"""
import base64
from unittest.mock import patch

import pytest
from flask_login import current_user

from app.auth import get_hash, require_scope
# noinspection PyUnresolvedReferences
from tests.fixtures import *

pytestmark = pytest.mark.usefixtures('legacy_database_seed')


@pytest.mark.unittest
def test_get_hash():
    """
    Really basic test of the hashing function.
    :return: N/A
    """
    hash1 = get_hash("SOME_RANDOM_TEXT_HERE")
    hash2 = get_hash("SOME_OTHER_RANDOM_TEXT_HERE")
    assert hash1 != hash2


@pytest.mark.unittest
def test_require_scope():
    """
    Tests the require scope function
    :return: N/A
    """
    with patch('app.auth.jwt') as mock_jwt:
        mock_jwt.get_unverified_claims.return_value = {
            'scope': 'read:signals read:stations'
        }
        actual = require_scope('read:signals', 'NOT_A_REAL_TOKEN')
        expected = True
        assert actual == expected

        actual = require_scope('write:admin', 'NOT_A_REAL_TOKEN')
        expected = False
        assert actual == expected


