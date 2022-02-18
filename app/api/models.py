""" api models

Flask-SQLAlchemy models for the Net API Backend
"""
# pylint: disable=too-few-public-methods
import datetime
import json
import os
import random
import sys
from collections.abc import Iterable

from functools import lru_cache
from typing import Optional, Union
from uuid import uuid4

from flask import current_app, request, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, UserMixin
from safrs import SAFRSBase
from safrs.jsonapi import SAFRSRestRelationshipAPI
from safrs.safrs_types import SAFRSID
from safrs.util import classproperty
from sqlalchemy import Column
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import RelationshipProperty, Session

from app.auth import require_scope, get_hash
from app.errors import AuthError, BadRequestError, get_scope_insufficient_error_message
from app.extensions import db
from .types import UserType

CLIENT_CONFIG = {
    "url": os.getenv("SOURCE_API_URL"),
    "auth0_client_id": os.getenv("SOURCE_API_AUTH0_CLIENT_ID"),
    "auth0_client_secret": os.getenv("SOURCE_API_AUTH0_CLIENT_SECRET"),
    "auth0_audience": os.getenv("SOURCE_API_AUTH0_AUDIENCE"),
    "auth0_url": "",
    "retries": 2
}

def generate_uid(prefix: str):
    """ Generate an iSP uid based on a prefix
        param prefix: A string prefix included in the uid
        return: A uid with a total prefix of "${prefix}-"
    """
    char_set = list('abcdefhjklmnopqrstuvwxyz23456789')
    return f'{prefix}-{"".join(random.choices(char_set, k=16))}'


class CustomSAFRSID(SAFRSID):
    """ Custom SAFRSID class
    """

    # pylint: disable=redefined-builtin
    @classmethod
    def validate_id(cls, id):
        if not id:
            return generate_uid(cls.__prefixid__)
        elif len(id) < 5:
            raise BadRequestError(f"Id field must be longer than 5 characters! Instead got {id}", 400)
        return id

    # pylint: disable=unsubscriptable-object
    # pylint: disable=no-member
    @classmethod
    def gen_id(cls):
        # This is the case if an autoincrement id is expected:
        if cls.columns and \
                len(cls.columns) == 1 and \
                cls.columns[0].type.python_type == int:
            return None

        return generate_uid(cls.__prefixid__)


def get_id_type(cls, super_class=SAFRSID) -> type:
    """
    get_id_type
    """
    columns = [col for col in cls.__table__.columns if col.primary_key]
    primary_keys = [col.name for col in columns]
    delimiter = getattr(cls, "delimiter", "_")
    __prefixid__ = cls.__prefixid__ if hasattr(
        cls, '__prefixid__') else cls.__name__.lower()
    id_type_class = type(
        cls.__name__ + "_ID", (super_class,), {
            "primary_keys": primary_keys,
            "columns": columns,
            "__prefixid__": __prefixid__,
            "delimiter": delimiter
        })
    return id_type_class


class BaseModel(SAFRSBase, db.Model):
    """ Base model
    """
    __abstract__ = True
    # Disable auto commit to play nice with flask-admin
    SAFRSBase.db_commit = False

    @classmethod
    def _s_sample_dict(cls):
        """
        :return: a sample to be used as an example "attributes" payload in the swagger example
        """
        sample_post_data = getattr(cls, 'sample_post_data',
                                   {'sample_post_data': 'not implemented'})
        return sample_post_data

class CustomRelationshipAPI(SAFRSRestRelationshipAPI):

    def require_write_permissions(self):
        #if current_user.type != UserType.write:
        #    raise AuthError(f'{current_user} is not authorized to perform that action', 403)
        pass

    def get(self, **kwargs):
        return super().get(**kwargs)


    def post(self, **kwargs):
        """
        Handles post requests for customer relationships
        """
        self.require_write_permissions()
        return super().post(**kwargs)

    def patch(self, **kwargs):
        """
        Handles patch requests for customer relationships
        """
        self.require_write_permissions()
        return super().patch(**kwargs)

    def delete(self, **kwargs):
        """
        Handles delete requests for station relationships
        """
        self.require_write_permissions()
        return super().delete(**kwargs)


class CustomIDModel(BaseModel):
    """ Custom ID model
    """
    __abstract__ = True
    __read_scope__ = ''
    __write_scope__ = ''

    _relationship_api = CustomRelationshipAPI

    @classmethod
    def validate_get(cls, **kwargs):
        """
        Validates incoming kwargs for a get request and raises errors if not valid.
        """
        pass

    def validate_patch(self, **attributes):
        """
        Validates incoming attributes for a patch request and raises errors if not valid.
        """
        pass

    @classmethod
    def validate_post(cls, id=None, **params):
        """
        Validates incoming params for a post request and raises errors if not valid.
        """
        pass

    def validate_delete(self):
        """
        Validates an incoming delete request and raises errors if not valid.
        """
        pass

    @classmethod
    def validate_get_instance_by_id(cls, id):
        """
        Validates an incoming get request by id and raises errors if not valid.
        """
        pass

    @classmethod
    def _s_get(cls, **kwargs):
        cls.validate_get(**kwargs)
        return super()._s_get(**kwargs)

    def _s_patch(self, **attributes):
        self.validate_patch(**attributes)
        return super()._s_patch(**attributes)

    # pylint: disable=redefined-builtin
    @classmethod
    def _s_post(cls, id=None, **params):
        cls.validate_post(id=id, **params)
        return super()._s_post(id=id, **params)

    def _s_delete(self):
        self.validate_delete()
        return super()._s_delete()

    # pylint: disable=unexpected-keyword-arg
    @classmethod
    def _s_get_instance_by_id(cls, id):
        cls.validate_get_instance_by_id(id=id)
        return super().get_instance(id=id)

    @classproperty
    @lru_cache(maxsize=32)
    # pylint: disable=no-self-argument
    def id_type(obj):
        """
        :return: the object's id type
        """
        id_type = get_id_type(obj, super_class=CustomSAFRSID)
        # monkey patch so we don't have to look it up next time
        obj.id_type = id_type
        return id_type


class User(db.Model, UserMixin):
    """ User model
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    token = db.Column(db.String(128), unique=True)
    type = db.Column(db.Enum(UserType), default=UserType.read)

    def __repr__(self):
        return f'<User {self.username}>'

    __str__ = __repr__


class Foo(CustomIDModel):
    """
        description: Represents a content owner.
    """
    __tablename__ = 'foos'
    __prefixid__ = 'foo'
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    sample_post_data = {}

    def __repr__(self) -> str:
        return f'<Foo {self.name}>'

    __str__ = __repr__


def register_admin_views(admin) -> None:
    """ Register models with the admin portal
    :return: None
    """

    class AuthModelView(ModelView):
        """ Model view with auth0 authentication
        """

        def is_accessible(self):
            return True

        def create_model(self, form):
            model = None
            try:
                model = self.model()
                form.populate_obj(model)
                if hasattr(model, '__prefixid__'):
                    model.id = generate_uid(model.__prefixid__)
                db.session.add(model)
                db.session.commit()
            except SQLAlchemyError as error:
                current_app.logger.error(str(error))
            return model

        def get_url(self, endpoint, **kwargs):
            """
            Generate URL for the endpoint. If you want to customize URL generation
            logic (persist some query string argument, for example), this is
            right place to do it.
            :param endpoint:
                Flask endpoint name
            :param kwargs:
                Arguments for `url_for`
            """
            admin_url_scheme = current_app.config['ADMIN_URL_SCHEME']
            return url_for(endpoint,
                           **kwargs,
                           _scheme=admin_url_scheme,
                           _external=True)

    class UserView(AuthModelView):
        """ Custom User View to allow token creation with a hash algorithm
        """
        create_template = 'admin/custom_user_create_view.html'

        def create_form(self, obj=None):
            """
            custom form to allow us to auto-generate a token
            """
            form = super().create_form()

            # this method is called twice, at load and submit of the form
            # this ensures we only generate the token once
            if not form.token.data:
                form.token.data = str(uuid4())

            return form

        def create_model(self, form):
            """
                Custom create view.
            """
            user = User()
            form.populate_obj(user)
            user.token = get_hash(form.token.data)
            db.session.add(user)
            db.session.commit()
            return user

    admin.add_view(UserView(User, db.session))
    admin.add_view(AuthModelView(Foo, db.session))
