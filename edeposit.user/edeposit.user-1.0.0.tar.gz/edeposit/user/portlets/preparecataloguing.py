# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from plone import api
from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from edeposit.content.originalfile import IOriginalFile
from edeposit.user import MessageFactory as _

class IPrepareDescriptiveCataloguing(IPortletDataProvider):
    pass

class IPrepareSubjectCataloguing(IPortletDataProvider):
    pass

class Assignment(base.Assignment):
    implements(IPrepareDescriptiveCataloguing)
    def __init__(self):
        pass
    @property
    def title(self):
        return _(u"Prepare Descriptive Cataloguing")

class AssignmentForDescriptiveCataloguing(base.Assignment):
    implements(IPrepareDescriptiveCataloguing)
    def __init__(self):
        pass
    @property
    def title(self):
        return _(u"Prepare Descriptive Cataloguing")

class AssignmentForSubjectCataloguing(base.Assignment):
    implements(IPrepareSubjectCataloguing)
    def __init__(self):
        pass
    @property
    def title(self):
        return _(u"Prepare Subject Cataloguing")

class RendererForDescriptiveCataloguing(base.Renderer):
    render = ViewPageTemplateFile('preparecataloguing.pt')

    def header(self):
        return _(u"Descriptive Cataloguing Preparing")
        
    def collectionPath(self):
        return '/'.join([api.portal.get().absolute_url(),'producents','originalfiles-waiting-for-descriptive-cataloguing-preparing'])

    def worklistPath(self):
        return '/'.join([api.portal.get().absolute_url(),'producents','worklist-waiting-for-descriptive-cataloguing-preparing'])

    def emailPath(self):
        return '/'.join([api.portal.get().absolute_url(),'producents','content_status_comment?workflow_action=sendEmailToDescriptiveCataloguingPreparing'])

    def collection01Path(self):
        return '/'.join([api.portal.get().absolute_url(),'producents','originalfiles-waiting-for-descriptive-cataloguing-review-preparing'])

    def worklist01Path(self):
        return '/'.join([api.portal.get().absolute_url(),'producents','worklist-waiting-for-descriptive-cataloguing-review-preparing'])

    def email01Path(self):
        return '/'.join([api.portal.get().absolute_url(),'producents','content_status_comment?workflow_action=sendEmailToDescriptiveCataloguingReviewPreparing'])

    def groupsAdministrationPath(self):
        return '/'.join([api.portal.get().absolute_url(),'producents','descriptive-cataloguing-groups-administration'])

    @property
    def available(self):
        return not IOriginalFile.providedBy(self.context)

class RendererForSubjectCataloguing(base.Renderer):
    render = ViewPageTemplateFile('preparecataloguing.pt')

    def header(self):
        return _(u"Subject Cataloguing Preparing")
        
    def collectionPath(self):
        return '/'.join([api.portal.get().absolute_url(),'producents','originalfiles-waiting-for-subject-cataloguing-preparing'])

    def worklistPath(self):
        return '/'.join([api.portal.get().absolute_url(),'producents','worklist-waiting-for-subject-cataloguing-preparing'])

    def emailPath(self):
        return '/'.join([api.portal.get().absolute_url(),'producents','content_status_comment?workflow_action=sendEmailToSubjectCataloguingPreparing'])

    def collection01Path(self):
        return '/'.join([api.portal.get().absolute_url(),'producents','originalfiles-waiting-for-subject-cataloguing-review-preparing'])

    def worklist01Path(self):
        return '/'.join([api.portal.get().absolute_url(),'producents','worklist-waiting-for-subject-cataloguing-review-preparing'])

    def email01Path(self):
        return '/'.join([api.portal.get().absolute_url(),'producents','content_status_comment?workflow_action=sendEmailToSubjectCataloguingReviewPreparing'])

    def groupsAdministrationPath(self):
        return '/'.join([api.portal.get().absolute_url(),'producents','subject-cataloguing-groups-administration'])
        
    @property
    def available(self):
        return not IOriginalFile.providedBy(self.context)

class AddFormForDescriptiveCataloguing(base.AddForm):
    form_fields = form.Fields(IPrepareDescriptiveCataloguing)

    def create(self, data):
        return AssignmentForDescriptiveCataloguing(**data)

class AddFormForSubjectCataloguing(base.AddForm):
    form_fields = form.Fields(IPrepareSubjectCataloguing)

    def create(self, data):
        return AssignmentForSubjectCataloguing(**data)

