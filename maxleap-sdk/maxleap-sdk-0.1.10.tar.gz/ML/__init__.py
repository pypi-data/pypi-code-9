# coding: utf-8

"""MaxLeap Python SDK
"""

import client
from .acl import ACL
from .client import init, by_hook, change_region, UserPrincipal, get_master_principal
from .errors import MaxLeapError
from .file_ import File
from .geo_point import GeoPoint
from .object_ import Object
from .query import Query
from .relation import Relation
from .user import User
from .role import Role
from .server import Server, get_principal
from .log import Log
from flask import Response

__author__ = 'czhou <czhou@ilegendsoft.com>'
__version__ = '0.1.1'
DEBUG = True
PRO = False

__all__ = [
    'ACL',
    'File',
    'GeoPoint',
    'MaxLeapError',
    'Object',
    'Query',
    'Relation',
    'User',
    'client',
    'init',
    'by_hook',
    'change_region',
    'UserPrincipal',
    'get_master_principal',
    'Role',
    'Server',
    'get_principal',
    'Log',
    'Response'
]
