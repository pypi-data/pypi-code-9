# -*- coding: utf-8 -*-
from plone import api
from plone.dexterity.utils import createContentInContainer, addContentToContainer, createContent
import uuid
from logging import getLogger
import itertools
from functools import reduce
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


logger = getLogger('edeposit.polici.wf_scripts')

def submitISBNChecks(wfStateInfo):
    logger.info("submitISBNChecks")
    print "submit isbn checks"
    epublication = wfStateInfo.object
    systemMessages = epublication['system-messages']
    originalFiles = epublication['original-files']
    isbns = filter(lambda item: item,
                   [epublication.isbn_souboru_publikaci] + \
                   [ii.isbn for ii in originalFiles.results()])

    with api.env.adopt_user(username="system"):
        for isbn in isbns:
            createContentInContainer(systemMessages, 'edeposit.content.isbnvalidationrequest',
                                     title = "Kontrola ISBN: " + isbn,
                                     isbn = isbn
                                 )
            
            createContentInContainer(systemMessages,  'edeposit.content.isbncountrequest',
                                     title = u"Zjištění duplicity ISBN: " + isbn,
                                     isbn = isbn
                                 )
            pass
        pass

def checkISBNsStatus(wfStateInfo):
    logger.info("checkISBNsStatus")
    print "check isbns status"
    epublication = wfStateInfo.object
    systemMessages = epublication['system-messages']
    originalFiles = epublication['original-files']
    wft = api.portal.get_tool('portal_workflow')
    isbns = filter(lambda item: item,
                   [epublication.isbn_souboru_publikaci] + \
                   [ii.isbn for ii in originalFiles.results()])

    def statusesForISBN(result,item):
        isbn,messages = item

        def findProperMessage(result, item):
            msg = item[1]
            if hasattr(msg,'is_valid'):
                result['is_valid'].add(msg.is_valid)
            if hasattr(msg,'num_of_records'): 
                result['num_of_records'].add(msg.num_of_records)
            return result

        statuses = reduce( findProperMessage, messages, {'is_valid':set(), 'num_of_records': set()} )
        result[isbn] = statuses
        return result
        
    statusesByISBN = reduce( statusesForISBN,
                          itertools.groupby(systemMessages.items(), key=lambda item: item[1].isbn),
                          dict() )
    
    with api.env.adopt_user(username="system"):
        # for each isbn must exists request and response in system
        # messages
        # isbns = ['978-0-306-40615-7',]
        # itemsByISBN = {'978-0-306-40615-7': {'num_of_records': set([0]), 'is_valid': set([True])}}
        # statuses = itemsByISBN['978-0-306-40615-7']
        
        def isbnStatus(itemsByISBN,isbn):
            statuses = itemsByISBN.get(isbn,{'num_of_records':set(),'is_valid':set()})
            return { 'is_valid': statuses['is_valid'],
                     'num_of_records': statuses['num_of_records'] }

        def statusISOK(status):
            return (status['is_valid'] == set([True]) and status['num_of_records'] == set([0]))
        
        isbnsWithError = filter(lambda isbn: not statusISOK(isbnStatus(statusesByISBN,isbn)), isbns)
        #if set([ii[1] for ii in isbnStatuses]) == set([True]):
        if not isbnsWithError:
            # vsechny ISBN jsou zkontrolovane
            print "all isbns are valid"
            wft.doActionFor(epublication, 'allISBNsAreValid')
            print "all files are virus free"
            wft.doActionFor(epublication,'allFilesAreVirusFree')
            print "all files has thumbnail"
            wft.doActionFor(epublication,'allThumbnailsOK')
            pass
        else:
            for (isbn,status) in map( lambda isbn: (isbn, isbnStatus(statusesByISBN,isbn)), isbnsWithError):
                if (status['num_of_records'] != set([]) and status['num_of_records'] != set([0])):
                    # duplicitni isbn
                    print "isbn je duplicitni: " + isbn
                if status['is_valid'] != set([]) and status['is_valid'] != set([True]):
                    # nevalidni zaznam
                    print "isbn neni validni: " + isbn
        pass
    pass


def submitAntivirusChecks(wfStateInfo):
    logger.info("submitAntivirusChecks")
    print "submit antivirus checks"
    epublication = wfStateInfo.object
    systemMessages = epublication['system-messages']
    originalFiles = epublication['original-files']

    with api.env.adopt_user(username="system"):
        for originalFile in originalFiles.results():
            # createContentInContainer(systemMessages, 'edeposit.content.isbnvalidationrequest',
            #                          title = "Kontrola ISBN: " + isbn,
            #                          isbn = isbn
            #                      )
            
            # createContentInContainer(systemMessages,  'edeposit.content.isbncountrequest',
            #                          title = u"Zjištění duplicity ISBN: " + isbn,
            #                          isbn = isbn
            #                      )
            pass
        pass

def submitExportToAleph(wfStateInfo):
    logger.info("submit export to Aleph")
    print "submit export to Aleph"
    epublication = wfStateInfo.object
    systemMessages = epublication['system-messages']
    originalFiles = epublication['original-files']

    with api.env.adopt_user(username="system"):
        for originalFile in originalFiles.results():
            createContentInContainer(systemMessages, 'edeposit.content.alephexportrequest',
                                     title = "Export do Alephu: " + originalFile.id,
                                     originalFileID = originalFile.id,
                                     isbn = originalFile.isbn,
                                 )
            pass
        pass


def checkExportStatuses(wfStateInfo):
    logger.info("checkExportStatuses")
    print "check export statuses"
    epublication = wfStateInfo.object
    systemMessages = epublication['system-messages']
    originalFiles = epublication['original-files']
    wft = api.portal.get_tool('portal_workflow')
    catalog = api.portal.get_tool('portal_catalog')
    folder_path = '/'.join(systemMessages.getPhysicalPath())
    exportResults = map(lambda brain: brain.getObject(), 
                        catalog(path={'query': folder_path, 'depth': 1},
                                portal_type = 'edeposit.content.alephexportresult')
                    )
    isbns = set(filter(lambda item: item, map(lambda ii: ii.isbn, originalFiles.results())))
    isbnsInExportResults = set(filter(lambda item: item, map(lambda result: result.isbn, exportResults)))
    with api.env.adopt_user(username="system"):
        # for each isbn must exists request and response in system messages
        if isbns == isbnsInExportResults:
            # vsechna ISBN jsou vyexportovana
            print "all isbns are exported"
            wft.doActionFor(epublication, 'allExportsToAlephOK')
            pass
        pass
    pass

def submitAlephRecordsLoad(wfStateInfo):
    logger.info("submitAlephRecordsLoad")
    print "submit aleph records load"
    wft = api.portal.get_tool('portal_workflow')
    epublication = wfStateInfo.object
    systemMessages = epublication['system-messages']
    originalFiles = epublication['original-files']
    isbns = frozenset([ii.isbn for ii in originalFiles.results() if ii.isbn])

    logger.info("submitSearchRequest")
    producer = getUtility(IProducer, name="amqp.isbn-search-request")
    with api.env.adopt_user(username="system"):
        for isbn in isbns:
            isbnq = ISBNQuery(isbn)
            request = SearchRequest(isbnq)
            producer.publish(serialize(request),
                             content_type = 'application/json',
                             headers = \
                             {'UUID': json.dumps({ \
                                                   'type': 'edeposit.epublication-load-aleph-records',
                                                   'value': { 'context_UID': str(epublication.UID()), 
                                                              'UID': 'search sysnumber for::' + isbn,
                                                          }
                                               })
                          }
            )
            wft.doActionFor(epublication, 'notifySystemAction', comment="Načtení záznamů z Alephu pro: " + isbn,)
            pass
        pass

def updateAlephRelatedData(wfStateInfo):
    wft = api.portal.get_tool('portal_workflow')
    epublication = wfStateInfo.object
    systemMessages = epublication['system-messages']
    originalFiles = epublication['original-files']
    for of in originalFiles:
        of.updateAlephRelatedData()
        #wft.doActionFor(of,'updateAlephRelatedData')
