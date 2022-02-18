""" api schema

SAFRS schema for Scaffold  API backend.
https://github.com/thomaxxl/safrs
"""

import os
from safrs import SAFRSAPI
from flask_login import login_required

from app.api.models import Foo
from app.utils import audit_logging

VERSION = os.getenv('BACKEND_VERSION', 'v1')


def create_api(app, host="0.0.0.0", port=8081, api_prefix=f"/api/{VERSION}"):
    """Helper factory function to create the API
    """
    api_description = """Provides relational data for scaffold
"""
    custom_swagger = {
        'host': app.config['SWAGGER_BASE_URL'],
        'info': {
            "title": 'ScaffoldAPI',
            "description": api_description,
            "version": "1.0",
        },
        'securityDefinitions': {
            "ApiKeyAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization",
            },
        },
        'security': [{
            'ApiKeyAuth': [],
        }],
    }
    api = SAFRSAPI(
        app,
        host=host,
        port=port,
        prefix=api_prefix,
        custom_swagger=custom_swagger,
    )

    properties = {"method_decorators": [audit_logging]}
    api.expose_object(Foo, **properties)
