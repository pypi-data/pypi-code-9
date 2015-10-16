# -*- coding: utf-8 -*-
from plone import api
from plone.dexterity.utils import createContentInContainer, addContentToContainer, createContent
import uuid
from logging import getLogger
import itertools
from zope.app.intid.interfaces import IIntIds
from z3c.relationfield import RelationValue
from Acquisition import aq_inner, aq_parent
from zope.component import queryUtility, getUtility, getAdapter
import base64
from edeposit.policy import MessageFactory as _

from edeposit.content.tasks import (
    IJSONEncoder,
    IPloneTaskSender,
    SendEmailWithWorklistToGroup,
    LoadSysNumbersFromAleph,
    RenewAlephRecords,
    SendEmailWithUserWorklist
)

from edeposit.content.amqp import IAMQPSender, IAMQPHandler

from collective.zamqp.interfaces import (
    IProducer, 
    IConsumer
)

import json
from five import grok

logger = getLogger('edeposit.producentfolder_wf_scripts')

# (occur-1 "def " nil (list (current-buffer)) "*Occur: originalfile_wf_scripts.py/def*")
# (occur-1 "class " nil (list (current-buffer)) "*Occur: originalfile_wf_scripts.py/class*")

def sendEmailToGroupAMQPFactory(view_name, recipients, groupname, subject):
    def handler(wfStateInfo):
        task = SendEmailWithWorklistToGroup (
            worklist = view_name,
            recipientsGroup = groupname,
            additionalEmails = recipients,
            subject = subject
        )
        IPloneTaskSender(task).send()
        
    return handler

# def sendEmailFactory(view_name, recipients, groupname, subject):
#     def handler(wfStateInfo):
#         context = wfStateInfo.object
#         view = api.content.get_view(name=view_name, context = context, request = context.REQUEST)
#         body = view()
#         if view.numOfRows:
#             emailsFromGroup = [aa.getProperty('email') for aa in api.user.get_users(groupname=groupname)]
#             for recipient in frozenset(emailsFromGroup + recipients):
#                 print "poslal jsem email: ", subject, recipient
#                 api.portal.send_email(recipient=recipient, subject=subject, body=body)
#         else:
#             print "zadny email jsem neposlal. prazdno. ", subject
            
#     return handler

sendEmailToISBNGeneration = sendEmailToGroupAMQPFactory("worklist-waiting-for-isbn-generation",
                                                        ['stavel.jan@gmail.com','alena.zalejska@pragodata.cz'],
                                                        'ISBN Agency Administrators',
                                                        "Dokumenty cekajici na prideleni ISBN")

sendEmailToISBNSubjectValidation = sendEmailToGroupAMQPFactory("worklist-waiting-for-isbn-subject-validation",
                                                               ['stavel.jan@gmail.com','alena.zalejska@pragodata.cz'],
                                                               'ISBN Agency Administrators',
                                                               "Dokumenty cekajici na vecnou kontrolu ISBN")

sendEmailWithOriginalFilesWaitingForAleph = sendEmailToGroupAMQPFactory("worklist-waiting-for-aleph",
                                                                        ['stavel.jan@gmail.com','alena.zalejska@pragodata.cz'],
                                                                        'Acquisitors',
                                                                        "Dokumenty cekajici na Aleph")

sendEmailToAcquisition = sendEmailToGroupAMQPFactory("worklist-waiting-for-acquisition",
                                                     ['stavel.jan@gmail.com','alena.zalejska@pragodata.cz'],
                                                     'Acquisitors',
                                                     "Dokumenty cekajici na Akvizici")

sendEmailWithOriginalFilesWaitingForProperAlephRecordChoosing = sendEmailToGroupAMQPFactory("worklist-waiting-for-proper-aleph-record-choosing",
                                                                                            ['stavel.jan@gmail.com','alena.zalejska@pragodata.cz'],
                                                                                            'Acquisitors',
                                                                                            "Dokumenty cekajici na vyber spravneho aleph zaznamu")

sendEmailToDescriptiveCataloguingPreparing \
    = sendEmailToGroupAMQPFactory("worklist-waiting-for-descriptive-cataloguing-preparing",
                                  ['stavel.jan@gmail.com','alena.zalejska@pragodata.cz'],
                                  'Descriptive Cataloguing Administrators',
                                  "Dokumenty cekajici na přípravu jmenného popisu")

sendEmailToDescriptiveCataloguingReviewPreparing \
    = sendEmailToGroupAMQPFactory("worklist-waiting-for-descriptive-cataloguing-review-preparing",
                                  ['stavel.jan@gmail.com','alena.zalejska@pragodata.cz'],
                                  'Descriptive Cataloguing Administrators',
                                  "Dokumenty cekajici na přípravu jmenné revize")

sendEmailToSubjectCataloguingPreparing \
    = sendEmailToGroupAMQPFactory("worklist-waiting-for-subject-cataloguing-preparing",
                                  ['stavel.jan@gmail.com','alena.zalejska@pragodata.cz'],
                                  'Subject Cataloguing Administrators',
                                  "Dokumenty cekajici na přípravu věcného popisu")

sendEmailToSubjectCataloguingReviewPreparing \
    = sendEmailToGroupAMQPFactory("worklist-waiting-for-subject-cataloguing-review-preparing",
                                  ['stavel.jan@gmail.com','alena.zalejska@pragodata.cz'],
                                  'Subject Cataloguing Administrators',
                                  "Dokumenty cekajici na přípravu věcné revize")

def queryForStates(portal_type='edeposit.content.originalfile', *args):
    return [ {'i': 'portal_type',
              'o': 'plone.app.querystring.operation.selection.is',
              'v': [portal_type]},
             {'i': 'review_state',
              'o': 'plone.app.querystring.operation.selection.is',
              'v': args},
             # {'i': 'path',
             #  'o': 'plone.app.querystring.operation.string.relativePath',
             #  'v': '../'}
             ]
    
def createGroupUsersCollections(context, groupname, indexName, state, readerGroup):
    members = api.user.get_users(groupname=groupname)
    for username in map(lambda member: member.id, members):
        coll = context.createUserCollection(username, indexName, state, readerGroup)

def sendEmailToGroupPersonsAMQPFactory(groupname, title, additionalEmails):
    def sendEmailToGroupPersons(wfStateInfo):
        task = SendEmailWithUserWorklist (
            groupname = groupname,
            additionalEmails = additionalEmails,
            title = title
        )
        IPloneTaskSender(task).send()

    return sendEmailToGroupPersons


sendEmailToGroupDescriptiveCataloguers = sendEmailToGroupPersonsAMQPFactory(
    groupname="Descriptive Cataloguers",
    title = u"Jmenný popis",
    additionalEmails = ['stavel.jan@gmail.com','alena.zalejska@pragodata.cz'],
)

sendEmailToGroupDescriptiveCataloguingReviewers = sendEmailToGroupPersonsAMQPFactory(
    groupname='Descriptive Cataloguing Reviewers',
    title = u"Revize JP",
    additionalEmails = ['stavel.jan@gmail.com','alena.zalejska@pragodata.cz'],
)

sendEmailToGroupSubjectCataloguers = sendEmailToGroupPersonsAMQPFactory(
    groupname='Subject Cataloguers', 
    title=u"Věcný popis",
    additionalEmails = ['stavel.jan@gmail.com','alena.zalejska@pragodata.cz'],
)

sendEmailToGroupSubjectCataloguingReviewers = sendEmailToGroupPersonsAMQPFactory(
    groupname='Subject Cataloguing Reviewers', 
    title=u"Revize VP",
    additionalEmails = ['stavel.jan@gmail.com','alena.zalejska@pragodata.cz'],
)

collections = [
    dict( name = "originalfiles-waiting-for-isbn-generation",
          title= u"Originály čekající na přidělení ISBN",
          query= queryForStates('ISBNGeneration'),
          group = 'ISBN Agency Members'),
    dict( name = "originalfiles-waiting-for-aleph",
          title= u"Originály čekající na Aleph",
          query= queryForStates('waitingForAleph'),
          group = 'Acquisition Administrators'),
    dict( name = "originalfiles-waiting-for-acquisition",
          title= u"Originály čekající na Akvizici",
          query= queryForStates('acquisition'),
          group = 'Acquisitors'),
    dict( name = "originalfiles-waiting-for-isbn-subject-validation",
          title= u"Originály čekající na věcnou kontrolu ISBN",
          query= queryForStates('ISBNSubjectValidation'),
          group= 'ISBN Agency Members'),
    dict( name = "originalfiles-waiting-for-descriptive-cataloguing-preparing",
          title= u"Originály čekající na přípravu jmenné katalogizace",
          query= queryForStates('descriptiveCataloguingPreparing'),
          group= 'Descriptive Cataloguing Administrators'),
    dict( name = "originalfiles-waiting-for-descriptive-cataloguing-review-preparing",
          title= u"Originály čekající na přípravu jmenné revize",
          query= queryForStates('descriptiveCataloguingReviewPreparing'),
          group= 'Descriptive Cataloguing Administrators'),
    
    # -- closed originalfiles that should be fully catalogized --
    dict( name = "originalfiles-waiting-for-closed-descriptive-cataloguing-preparing",
          title= u"Zamčené originály čekající na přípravu jmenné katalogizace",
          query= queryForStates('closedDescriptiveCataloguingPreparing') + \
              [{'i': 'shouldBeFullyCatalogized',
                'o': 'plone.app.querystring.operation.boolean.isTrue'}],
          group= 'Descriptive Cataloguing Administrators',
          ),
    dict( name = "originalfiles-waiting-for-closed-descriptive-cataloguing-review-preparing",
          title= u"Zamčené originály čekající na přípravu jmenné revize",
          query= queryForStates('closedDescriptiveCataloguingReviewPreparing') +\
              [{'i': 'shouldBeFullyCatalogized',
                'o': 'plone.app.querystring.operation.boolean.isTrue'}],
          group= 'Descriptive Cataloguing Administrators',
          ),
    # ----------------------------------------------------------------
    dict( name = "originalfiles-waiting-for-subject-cataloguing-preparing",
          title= u"Originály čekající na přípravu věcné katalogizace",
          query= queryForStates('subjectCataloguingPreparing'),
          group= 'Subject Cataloguing Administrators',
          ),
    dict( name = "originalfiles-waiting-for-subject-cataloguing-review-preparing",
          title= u"Originály čekající na přípravu věcné revize",
          query= queryForStates('subjectCataloguingReviewPreparing'),
          group= 'Subject Cataloguing Administrators',
          ),
    # -- closed originalfiles that should be fully catalogized --
    dict( name = "originalfiles-waiting-for-closed-subject-cataloguing-preparing",
          title= u"Zamčené originály čekající na přípravu věcné katalogizace",
          query= queryForStates('closedSubjectCataloguingPreparing') +\
              [{'i': 'shouldBeFullyCatalogized',
                'o': 'plone.app.querystring.operation.boolean.isTrue'}],
          group= 'Subject Cataloguing Administrators',
          ),
    dict( name = "originalfiles-waiting-for-closed-subject-cataloguing-review-preparing",
          title= u"Zamčené originály čekající na přípravu věcné revize",
          query= queryForStates('closedSubjectCataloguingReviewPreparing') +\
              [{'i': 'shouldBeFullyCatalogized',
                'o': 'plone.app.querystring.operation.boolean.isTrue'}],
          group= 'Subject Cataloguing Administrators',
          ),
    # ----------------------------------------------------------------
    dict( name = "originalfiles-waiting-for-proper-aleph-record-choosing",
          title= u"Originály čekající na výběr správného aleph záznamu",
          query= queryForStates('chooseProperAlephRecord'),
          group= 'Acquisitors',
          ),
    dict( name = "my-producents",
          title= u"Moji producenti",
          query= [ {'i': 'portal_type',
                    'o': 'plone.app.querystring.operation.selection.is',
                    'v': ['edeposit.user.producent']},
                   {'i': 'getAssignedProducentEditors',
                    'o': 'plone.app.querystring.operation.string.currentUser',
                    'v': []},
                   ],
          group= 'Producent Editors',
          ),
    dict( name = "originalfiles-waiting-for-renew-aleph-records",
          title= u"Originály čekající na akci v Alephu",
          query= queryForStates(
            'acquisition',
            'ISBNSubjectValidation',
            'subjectCataloguing',
            'subjectCataloguingReview',
            'descriptiveCataloguing',
            'descriptiveCataloguingReview',
            'chooseProperAlephRecord',
            'closedDescriptiveCataloguingReviewPreparing',
            "closedDescriptiveCataloguingReview",
            "closedSubjectCataloguingPreparing",
            "closedSubjectCataloguing",
            "closedSubjectCataloguingReviewPreparing",
            "closedSubjectCataloguingReview",
            ),
          group= 'Subject Cataloguing Administrators',
          ),
    ]


def recreateCollections(wfStateInfo):
    context = wfStateInfo.object
    for collection in collections:
        name = collection['name']
        if name not in context.keys():
            content = api.content.create (
                id=name,
                container=context,
                type='Collection', 
                title=collection['title'],
                query=collection['query']
            )
            api.group.grant_roles(groupname=collection['group'],
                                  roles=['Reader',],
                                  obj=content)
            
    createGroupUsersCollections(context=context, 
                                groupname="Descriptive Cataloguers",
                                indexName="getAssignedDescriptiveCataloguer",
                                state="descriptiveCataloguing",
                                readerGroup = "Descriptive Cataloguing Administrators",
                            )

    createGroupUsersCollections(context=context, 
                                groupname="Descriptive Cataloguing Reviewers",
                                indexName="getAssignedDescriptiveCataloguingReviewer",
                                state="descriptiveCataloguingReview",
                                readerGroup = "Descriptive Cataloguing Administrators",
                            )

    createGroupUsersCollections(context=context, 
                                groupname="Subject Cataloguers",
                                indexName="getAssignedSubjectCataloguer",
                                state="subjectCataloguing",
                                readerGroup = "Subject Cataloguing Administrators",
                            )

    createGroupUsersCollections(context=context, 
                                groupname="Subject Cataloguing Reviewers",
                                indexName="getAssignedSubjectCataloguingReviewer",
                                state="subjectCataloguingReview",
                                readerGroup = "Subject Cataloguing Administrators",
                                )
    
    if not context.has_key('my-epublications'):
        context.invokeFactory('Collection','my-epublications', 
                              title=u"Moje ohlášené ePublikace",
                              query=[{'i': 'portal_type', 
                                      'o': 'plone.app.querystring.operation.selection.is', 
                                      'v': ['edeposit.content.originalfile',]
                                      },
                                     {'i': 'getAssignedProducentEditors',
                                      'o': 'plone.app.querystring.operation.string.currentUser', 
                                      'v': []},
                                     ],
                              )
    pass

def loadSysNumbersFromAleph(wfStateInfo):
    IPloneTaskSender(LoadSysNumbersFromAleph()).send()

def renewAlephRecords(wfStateInfo):
    IPloneTaskSender(RenewAlephRecords()).send()
