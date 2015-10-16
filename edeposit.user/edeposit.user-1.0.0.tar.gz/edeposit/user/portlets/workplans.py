# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
import urllib

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone import api
from edeposit.content.originalfile import IOriginalFile
from edeposit.user import MessageFactory as _
from itertools import repeat

class Renderer(base.Renderer):
    groupName = "Administrators"
    portalHeader = "Some Title"
    groupEmailTransition = "sendEmailToGroupSubjectCataloguers"
    render = ViewPageTemplateFile('workplans.pt')
    review_state = 'descriptiveCataloguing'
    assigned_person_index = "getAssignedDescriptiveCataloguer"

    def groupUsers(self):
        users = api.user.get_users(groupname=self.groupName)
        return users
        
    def urlOfGroupEmail(self):
        return '/'.join(api.portal.get().getPhysicalPath() + ('producents','content_status_comment')) \
            + "?workflow_action=%s" % (self.groupEmailTransition,)

    def collectionPath(self, user):
        #collName =  "/producents/originalfiles-waiting-for-user-" + user.id
        #return '/'.join(api.portal.get().getPhysicalPath() + ('producents',collName))
        worklistName = "worklist-by-state-waiting-for-user"

        urlArgs = zip(repeat('review_state'), 
                      isinstance(self.review_state,str) and [self.review_state] or self.review_state) \
                      +  [('assigned_person_index',self.assigned_person_index),('userid', user.id)]

        url = '/'.join(api.portal.get().getPhysicalPath() + ('producents', worklistName)) + "?" + urllib.urlencode(urlArgs)
        return url

    def userFullname(self,user):
        return user.getProperty("fullname")

    def numOfOriginalFilesWaitingForUser(self, user):
        #viewName = "worklist-by-state-waiting-for-user"
        #collName =  "/producents/originalfiles-waiting-for-user-" + user.id
        #collection = api.content.get(path=collName)
        #return collection and len(collection.results(batch=False)) or 0
        worklistName = "worklist-by-state-waiting-for-user"
        producentsFolder = api.portal.get_tool('portal_catalog')(portal_type='edeposit.user.producentfolder')[0].getObject()
        request = self.context.REQUEST
        request['userid'] = user.id
        request['review_state'] = self.review_state
        request['assigned_person_index'] = self.assigned_person_index
        view = api.content.get_view(name=worklistName,
                                    request = request,
                                    context=producentsFolder)
        results = view.getResults()
        return len(results)

    def linkText(self,user):
        return "%s (%d)" % (self.userFullname(user), self.numOfOriginalFilesWaitingForUser(user))

    def header(self):
        return self.portalHeader

    @property
    def available(self):
        return not IOriginalFile.providedBy(self.context)

class RendererForDescriptiveCataloguers(Renderer):
    groupName = "Descriptive Cataloguers"
    portalHeader = u"Práce pro jmenný popis"
    groupEmailTransition = "sendEmailToGroupDescriptiveCataloguers"
    review_state = ("descriptiveCataloguing","closedDescriptiveCataloguing")
    assigned_person_index = 'getAssignedDescriptiveCataloguer'

class RendererForDescriptiveReviewers(Renderer):
    groupName = "Descriptive Cataloguing Reviewers"
    portalHeader = u"Práce pro revizi jmenného popisu"
    groupEmailTransition = "sendEmailToGroupDescriptiveCataloguingReviewers"
    review_state = ("descriptiveCataloguingReview","closedDescriptiveCataloguingReview")
    assigned_person_index = 'getAssignedDescriptiveCataloguingReviewer'

class RendererForSubjectCataloguers(Renderer):
    groupName = "Subject Cataloguers"
    portalHeader = u"Práce pro věcný popis"
    groupEmailTransition = "sendEmailToGroupSubjectCataloguers"
    review_state = ("subjectCataloguing","closedSubjectCataloguing")
    assigned_person_index = 'getAssignedSubjectCataloguer'

class RendererForSubjectReviewers(Renderer):
    groupName = "Subject Cataloguing Reviewers"
    portalHeader = u"Práce pro revizi věcného popisu"
    groupEmailTransition = "sendEmailToGroupSubjectCataloguingReviewers"
    review_state = ("subjectCataloguingReview","closedSubjectCataloguingReview")
    assigned_person_index = 'getAssignedSubjectCataloguingReviewer'

class IWorkPlansForDescriptiveCataloguers(IPortletDataProvider):
    pass

class IWorkPlansForDescriptiveReviewers(IPortletDataProvider):
    pass

class IWorkPlansForSubjectCataloguers(IPortletDataProvider):
    pass

class IWorkPlansForSubjectReviewers(IPortletDataProvider):
    pass

class Assignment(base.Assignment):
    implements(IWorkPlansForDescriptiveCataloguers)
    def __init__(self):
        pass
    @property
    def title(self):
        return _(u"Some Assignment")

class AssignmentForDescriptiveCataloguers(base.Assignment):
    implements(IWorkPlansForDescriptiveCataloguers)
    def __init__(self):
        pass
    @property
    def title(self):
        return _(u"Work Plans for Descriptive Cataloguers")

class AssignmentForDescriptiveReviewers(base.Assignment):
    implements(IWorkPlansForDescriptiveReviewers)
    def __init__(self):
        pass
    @property
    def title(self):
        return _(u"Work Plans for Descriptive Reviewers")

class AssignmentForSubjectCataloguers(base.Assignment):
    implements(IWorkPlansForSubjectCataloguers)
    def __init__(self):
        pass
    @property
    def title(self):
        return _(u"Work Plans for Subject Cataloguers")

class AssignmentForSubjectReviewers(base.Assignment):
    implements(IWorkPlansForSubjectReviewers)
    def __init__(self):
        pass
    @property
    def title(self):
        return _(u"Work Plans for Subject Reviewers")

class AddFormForDescriptiveCataloguers(base.AddForm):
    form_fields = form.Fields(IWorkPlansForDescriptiveCataloguers)
    def create(self, data):
        return AssignmentForDescriptiveCataloguers(**data)

class AddFormForDescriptiveReviewers(base.AddForm):
    form_fields = form.Fields(IWorkPlansForDescriptiveReviewers)
    def create(self, data):
        return AssignmentForDescriptiveReviewers(**data)

class AddFormForSubjectCataloguers(base.AddForm):
    form_fields = form.Fields(IWorkPlansForSubjectCataloguers)
    def create(self, data):
        return AssignmentForSubjectCataloguers(**data)

class AddFormForSubjectReviewers(base.AddForm):
    form_fields = form.Fields(IWorkPlansForSubjectReviewers)
    def create(self, data):
        return AssignmentForSubjectReviewers(**data)


