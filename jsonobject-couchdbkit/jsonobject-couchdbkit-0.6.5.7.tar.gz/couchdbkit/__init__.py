# -*- coding: utf-8 -
#
# This file is part of couchdbkit released under the MIT license.
# See the NOTICE for more information.

from .version import version_info, __version__

from .resource import  RequestFailed, CouchdbResource
from .exceptions import InvalidAttachment, DuplicatePropertyError,\
BadValueError, MultipleResultsFound, NoResultFound, ReservedWordError,\
DocsPathNotFound, BulkSaveError, ResourceNotFound, ResourceConflict, \
PreconditionFailed

from .client import Server, Database, ViewResults
from .changes import ChangesStream
from .consumer import Consumer
from .designer import document, push, pushdocs, pushapps, clone
from .external import External
from .loaders import BaseDocsLoader, FileSystemDocsLoader

from .schema import (
    Property, IntegerProperty, DecimalProperty, BooleanProperty, FloatProperty, StringProperty,
    DateTimeProperty, DateProperty, TimeProperty,
    dict_to_json, dict_to_json, dict_to_json,
    dict_to_python,
    DocumentSchema, DocumentBase, Document, StaticDocument, contain,
    QueryMixin, AttachmentMixin,
    SchemaProperty, SchemaListProperty, SchemaDictProperty,
    ListProperty, DictProperty, StringDictProperty, StringListProperty, SetProperty
)

import logging

LOG_LEVELS = {
    "critical": logging.CRITICAL,
    "error": logging.ERROR,
    "warning": logging.WARNING,
    "info": logging.INFO,
    "debug": logging.DEBUG
}

def set_logging(level, handler=None):
    """
    Set level of logging, and choose where to display/save logs
    (file or standard output).
    """
    if not handler:
        handler = logging.StreamHandler()

    loglevel = LOG_LEVELS.get(level, logging.INFO)
    logger = logging.getLogger('couchdbkit')
    logger.setLevel(loglevel)
    format = r"%(asctime)s [%(process)d] [%(levelname)s] %(message)s"
    datefmt = r"%Y-%m-%d %H:%M:%S"

    handler.setFormatter(logging.Formatter(format, datefmt))
    logger.addHandler(handler)

