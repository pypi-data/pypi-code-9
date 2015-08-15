"""
Shared values

Copyright 2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import re
import sys

import validators as v
from .custom_validators import content_type


PY3 = sys.version_info >= (3, 0, 0)
if PY3:
    str_type = str
else:
    str_type = basestring

CONTENT_ID_RE = re.compile(r'^[0-9a-f]{32}$', re.I)
PLACEHOLDER_RE = re.compile(r'^\$[A-Z]+$')
LOCALE_RE = re.compile(r'^[a-z]{2}([_-][a-zA-Z]+)?$', re.I)
COMMASEP_RE = re.compile(r'^[\w ]+(?:, ?[\w ]+)*$', re.U)
RELPATH_RE = re.compile(r'^[^/]+(/[^/]+)*$')
SIZE_RE = re.compile(r'\d+x\d+')
TS_FMT = '%Y-%m-%d %H:%M:%S UTC'
DATE_FMT = '%Y-%m-%d'
LICENSES = ('CC-BY', 'CC-BY-ND', 'CC-BY-NC', 'CC-BY-ND-NC', 'CC-BY-SA',
            'CC-BY-NC-SA', 'GFDL', 'OPL', 'OCL', 'ADL', 'FAL', 'PD', 'OF',
            'ARL', 'ON')
LICENSE_NAMES = (
    'Creative Commons Attribution',
    'Creative Commons Attribution-NoDerivs',
    'Creative Commons Attribution-NonCommercial',
    'Creative Commons Attribution-NonCommercial-NoDerivs',
    'Creative Commons Attribution-ShareAlike',
    'Creative Commons Attribution-NonCommercial-ShareAlike',
    'GNU Free Documentation License',
    'Open Publication License',
    'Open Content License',
    'Against DRM License',
    'Free Art License',
    'Public Domain',
    'Other free license',
    'All rights reserved',
    'Other non-free license',
)
LICENSE_PAIRS = dict(zip(LICENSES, LICENSE_NAMES))

REQUIRED = (
    'title',
    'url',
    'timestamp',
    'broadcast',
    'license',
)

OPTIONAL = (
    'archive',
    'images',
    'index',
    'is_partner',
    'is_sponsored',
    'keep_formatting',
    'keywords',
    'language',
    'multipage',
    'publisher',
    'replaces',
    'thumbnail',
    'cover',
    'content',
)

KEYS = REQUIRED + OPTIONAL

DEFAULTS = {
    'archive': 'core',
    'index': 'index.html',
    'is_partner': False,
    'is_sponsored': False,
    'keywords': '',
    'language': '',
    'multipage': False,
    'publisher': '',
    'content': { 'html': {} },
}

TYPE_SPECS = {
    'html': {
        'main': [v.required, v.match(RELPATH_RE)],
        'keep_formatting': [v.optional(), v.istype(bool)],
        },
    'video': {
        'main': [v.required, v.match(RELPATH_RE)],
        'description': [v.optional(), v.instanceof(str_type)],
        'duration': [v.optional(), v.istype(int), v.gte(1)],
        'size': [v.optional(), v.match(SIZE_RE)],
        },
    'audio': {
        'description': [v.optional(), v.instanceof(str_type)],
        'playlist': [v.required, v.istype(list),
                     v.min_len()],
        },
    'audio.playlist': {
        'file': [v.required, v.instanceof(str_type), v.match(RELPATH_RE)],
        'title': [v.optional(), v.instanceof(str_type)],
        'duration': [v.optional(), v.istype(int), v.gte(1)],
        },
    'image': {
        'description': [v.optional(), v.instanceof(str_type)],
        'album': [v.required, v.istype(list), v.min_len()],
        },
    'image.album': {
        'file': [v.required, v.instanceof(str_type), v.match(RELPATH_RE)],
        'title': [v.optional(), v.instanceof(str_type)],
        'thumbnail': [v.optional(), v.instanceof(str_type)],
        'caption': [v.optional(), v.instanceof(str_type)],
        'size': [v.optional(), v.match(SIZE_RE)],
        'description': [v.optional(), v.instanceof(str_type)],
        },
    'generic': {
        'description': [v.optional(), v.instanceof(str_type)],
        },
    'app': {
        'description': [v.optional(), v.instanceof(str_type)],
        'version': [v.optional(), v.instanceof(str_type)],
        },
  }

SPECS = {
    'keep_formatting': [v.deprecated],
    'multipage': [v.deprecated],
    'images': [v.deprecated],
    'index': [v.deprecated],
    'title': [v.required, v.nonempty],
    'url': [v.required, v.nonempty, v.url],
    'timestamp': [v.required, v.nonempty, v.timestamp(TS_FMT)],
    'broadcast': [v.required, v.nonempty,
                  v.OR(v.timestamp(DATE_FMT), v.match(PLACEHOLDER_RE))],
    'license': [v.required, v.isin(LICENSES)],
    'language': [v.optional(''), v.nonempty, v.match(LOCALE_RE)],
    'keywords': [v.optional(''), v.nonempty, v.match(COMMASEP_RE)],
    'archive': [v.optional(''), v.nonempty],
    'publisher': [v.optional(''), v.nonempty],
    'is_partner': [v.optional(), v.istype(bool)],
    'is_sponsored': [v.optional(), v.istype(bool)],
    'replaces': [v.optional(''), v.match(CONTENT_ID_RE)],
    'thumbnail': [v.optional(''), v.match(RELPATH_RE)],
    'cover': [v.optional(''), v.match(RELPATH_RE)],
    'content': [v.optional(), v.nonempty, v.istype(dict),
                content_type(TYPE_SPECS)],
}
