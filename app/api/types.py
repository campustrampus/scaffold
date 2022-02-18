"""
 The attribute name is what gets stored in the database by SQLAlchemy and
 the attribute value is what is serialized in JSON output over the API
 endpoints

 All of these enum types have lowercase attribute names so that
 SQLAlchemy stores them in the database in all lowercase without having to
 implement callable_values in every database column mapping for enums.
"""


import enum

@enum.unique
class UserType(str, enum.Enum):
    oauth = 'oauth'
    read = 'read'
    write = 'write'
