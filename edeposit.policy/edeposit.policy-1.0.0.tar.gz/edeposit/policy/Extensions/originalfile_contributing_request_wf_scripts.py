# -*- coding: utf-8 -*-
from plone import api
from plone.dexterity.utils import createContentInContainer, addContentToContainer, createContent
import uuid
from logging import getLogger
import itertools
from functools import reduce
from Acquisition import aq_inner, aq_parent
from five import grok
from zope.component import queryUtility, getUtility
from z3c.relationfield import RelationValue
from zope.app.intid.interfaces import IIntIds

from edeposit.amqp.aleph import (
    ISBNQuery, 
    GenericQuery, 
    CountRequest, 
    SearchRequest, 
    DocumentQuery,
    ISBNValidationRequest,
    ExportRequest
)
from edeposit.amqp.serializers import (
    serialize,
    deserialize
)
from edeposit.amqp.aleph.datastructures.epublication import (
    EPublication,
    Author
)

from edeposit.amqp.aleph.datastructures.results import (
    ISBNValidationResult,
    CountResult,
    SearchResult,
    ExportResult,
)
from collective.zamqp.interfaces import (
    IProducer, 
    IBrokerConnection,
    IConsumer,
    IMessageArrivedEvent
)
from collective.zamqp.producer import Producer
from collective.zamqp.consumer import Consumer
from collective.zamqp.connection import BlockingChannel
import json

logger = getLogger('edeposit.originalfile_contributing_request.wf_scripts')

# class ISBNSearchRequestProducent(Producer):
#     grok.name('amqp.isbn-search-request')

#     connection_id = "aleph"
#     exchange = "search"
#     serializer = "text/plain"
#     exchange_type = "topic"
#     exchange_durable = True
#     auto_delete = False
#     durable = True
#     routing_key = "request"
#     pass

def submitSearchRequest(wfStateInfo):
    logger.info("submitSearchRequest")
    context = wfStateInfo.object
    isbnq = ISBNQuery(context.isbn)
    request = SearchRequest(isbnq)
    producer = getUtility(IProducer, name="amqp.isbn-search-request")
    producer.publish(serialize(request),
                     content_type = 'application/json',
                     headers = \
                     {'UUID': json.dumps({ \
                                           'type': 'edeposit.originalfile-search-alephrecords-request',
                                           'value': { 'context_UID': str(context.UID()), 
                                                      'UID': 'search-isbn:' + context.isbn
                                                 }
                                       })
                  }
                 )

def loadAnEPublication(wfStateInfo):
    logger.info("load an ePublication")
    context = wfStateInfo.object
    aleph_record = context.choosen_aleph_record.to_object
    doc_id = aleph_record.aleph_sys_number
    library = aleph_record.aleph_library
    request = SearchRequest(DocumentQuery(doc_id=doc_id, library=library))
    producer = getUtility(IProducer, name="amqp.sysnumber-search-request")
    producer.publish(serialize(request),
                     content_type = 'application/json',
                     headers = \
                     {'UUID': json.dumps({ \
                                           'type': 'edeposit.originalfile-load-epublication-request',
                                           'value': { 'context_UID': str(context.UID()), 
                                                      'UID': 'search-sysnumber:' + str(doc_id) + "/" + str(library)
                                                  }
                                       })
                  }
                 )

def tryToChooseARecord(wfStateInfo):
    """ if there is just one record got from Aleph,
    choose it as primary record and calls next transition

    If there are more records got from Aleph, this function does not do anything.
    """
    context = wfStateInfo.object
    items = context.listFolderContents(contentFilter={"portal_type" : "edeposit.content.alephrecord"})
    if len(items) == 1:
        """ choose this record as primary """
        print "choosing this record as primary one"
        intids = getUtility(IIntIds)
        context.choosen_aleph_record = RelationValue(intids.getId(items[0]))
        wft = api.portal.get_tool('portal_workflow')
        wft.doActionFor(context, 'loadAnEPublication')
    pass

