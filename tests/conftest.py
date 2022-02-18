""" tests conftest

Configuration fixtures for pytest
"""

import base64

import pytest
from flask import Flask
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session

from app import create_app, create_celery, init_sql_db, User, get_hash
from app.extensions import db
from app.api.types import UserType
from .utils import get_session

# This enables the celery fixtures for pytest
# pylint: disable=invalid-name
pytest_plugins = ("celery.contrib.pytest")


@pytest.fixture(scope='module')
def app() -> Flask:
    """Create and configure a new app instance for each test."""
    scaffold_app = create_app()
    ctx = scaffold_app.app_context()
    ctx.push()

    yield scaffold_app

    ctx.pop()


@pytest.fixture(scope='module')
def client(app: Flask) -> FlaskClient:
    """Create a client with context."""
    yield app.test_client()


@pytest.fixture(scope='module')
def auth_headers():
    """ Authentication headers"""
    token = 'admintoken123'
    b64_value = base64.b64encode(token.encode('utf-8')).decode()
    headers = {
        "Authorization": f'Basic {b64_value}',
        "Content-Type": "application/vnd.api+json",
        "Accept": "application/vnd.api+json",
    }

    yield headers


@pytest.fixture
def celery_app():
    """Create and configure a new celery instance for each test."""
    net_celery = create_celery()

    yield net_celery


@pytest.fixture
def celery_worker_parameters():
    """Set worker parameters to not perform a ping check
    """
    return {
        'perform_ping_check': False,
    }


def session():
    """Creates a requests sessions for use with integration testing
    """
    yield get_session()


@pytest.fixture(scope='module')
def database(app) -> SQLAlchemy:
    return db


@pytest.fixture(scope='function')
@pytest.mark.usefixtures('app')
def db_session(database: SQLAlchemy) -> Session:
    database.create_all()

    # Need to seed this to allow login
    admin_user = User(username="admin", token=get_hash("admintoken123"), type=UserType.write)
    database.session.add(admin_user)
    database.session.commit()

    yield database.session

    database.session.close()
    database.drop_all()


@pytest.fixture(scope='function')
@pytest.mark.usefixtures('app')
def db_seeded_session(database) -> Session:
    init_sql_db(drop=True)

    # Make sure we have a clean session to start with
    database.session.close()

    return database.session
