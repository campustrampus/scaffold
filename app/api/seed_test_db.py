""" seed_test_db

Helper functions to seed test data in the database
"""
import re
from typing import Any

from faker import Faker
from faker.providers import internet, company, misc

from app.auth import get_hash
from app.extensions import db
from app.api.models import Foo, User
from app.api.types import UserType

SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'

_all_foos: list[Foo] = []

re_normalize_name = re.compile('([^A-Za-z])')


# pylint: disable=maybe-no-member, too-many-locals, too-many-statements
def init_sql_db(drop: bool) -> None:
    """ Initialize the database with test data
    :return: None
    """
    fake = Faker()

    if drop:
        db.drop_all()
        db.create_all()

    admin_user = User(username="admin", token=get_hash("admintoken123"), type=UserType.write)
    db.session.add(admin_user)

    global _all_foos
    _all_foos = insert_foos()


def insert_foos() -> list[Foo]:
    foo_names = ['one_true_foo']

    foos = [Foo(name=f) for f in foo_names]
    db.session.add_all(foos)
    return foos

def get_random_choice(items: list) -> Any:
    fake = Faker()
    return fake.random_element(elements=items)


def get_random_choices(items: list) -> list[Any]:
    fake = Faker()
    return fake.random_elements(elements=items, unique=True)


def normalize_name(name: str):
    return re_normalize_name.sub(r'-', name.lower())
