""" api schema_docs

Swagger document dictionaries for asynchronous routes.
"""
error_responses = {
    "400": {
        "description": "Bad request syntax or unsupported method",
        "schema": {
            "$ref": "#/definitions/jsonapi_error_400"
        }
    },
    "403": {
        "description": "Forbidden",
        "schema": {
            "$ref": "#/definitions/jsonapi_error_403"
        }
    },
    "404": {
        "description": "Not Found",
        "schema": {
            "$ref": "#/definitions/jsonapi_error_404"
        }
    },
    "405": {
        "description": "Specified method is invalid for this resource",
        "schema": {
            "$ref": "#/definitions/jsonapi_error_405"
        }
    },
    "409": {
        "description": "Request Conflict",
        "schema": {
            "$ref": "#/definitions/jsonapi_error_409"
        }
    },
    "500": {
        "description": "Internal Server Error",
        "schema": {
            "$ref": "#/definitions/jsonapi_error_500"
        }
    },
}
