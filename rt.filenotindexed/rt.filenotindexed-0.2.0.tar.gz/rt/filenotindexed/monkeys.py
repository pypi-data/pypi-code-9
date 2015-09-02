# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger('rt.filenotindexed')

try:
    from Products.ATContentTypes.content.file import ATFileSchema
except ImportError:
    ATFileSchema = None

try:
    from plone.app.blob.subtypes.file import SchemaExtender as FileSchemaExtender
except ImportError:
    FileSchemaExtender = None

try:
    from plone.app.contenttypes.indexers import SearchableText_file as pac_SearchableText_file
except ImportError:
    pac_SearchableText_file = None


if ATFileSchema:
    ATFileSchema['file'].searchable = False
    logger.warning('Disabled indexing of ATFile')
if FileSchemaExtender:
    FileSchemaExtender.fields[0].searchable = False
    logger.warning('Disabled indexing of ATBlob')
if pac_SearchableText_file:
    from plone.app.contenttypes import indexers
    from plone.app.contenttypes.interfaces import IFile
    from plone.indexer.decorator import indexer
    
    @indexer(IFile)
    def pac_SearchableText_file(obj):
        return indexers.SearchableText(obj)

    indexers.SearchableText_file = pac_SearchableText_file
    logger.warning('Disabled indexing of plone.app.contenttypes File')

