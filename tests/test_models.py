"""
Test Source API models
"""
from unittest.mock import patch
from faker.proxy import Faker
from sqlalchemy.orm import Session

import pytest
from app.api.models import Foo

from app import UserType
from app.errors import AuthError, BadRequestError
# noinspection PyUnresolvedReferences
from tests.fixtures import *

pytestmark = pytest.mark.usefixtures('legacy_database_seed')


@pytest.mark.unittest
def test_foo_print(app):
    """ Test Interface Print
    """
    db_obj = Foo.query.one()

@pytest.mark.usefixtures('app')
def test_user_print():
    """ Test User Print
    """
    db_obj = User.query.one()
    assert '<User' in str(db_obj)


