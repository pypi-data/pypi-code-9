# -*- coding: utf-8 -*-
from plone.memoize.view import memoize
from zope.component import getMultiAdapter
from zope.deprecation.deprecation import deprecate
from zope.i18n import translate
from zope.interface import implements, alsoProvides, Interface
from zope.viewlet.interfaces import IViewlet

from AccessControl import getSecurityManager
from Acquisition import aq_base, aq_inner, aq_parent

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _
from plone.directives import form
from plone.app.layout.globals.interfaces import IViewView
from plone.app.layout.viewlets.interfaces import IContentViews, IBelowContent, IAboveContentBody, IBelowContentBody
from plone.app.layout.viewlets import ViewletBase

from plone import api
from edeposit.user.producent import IProducent

from plone.app.contentmenu import menu
from plone.app.contentmenu.interfaces import IWorkflowSubMenuItem
from plone.z3cform.layout import FormWrapper

from zope.publisher.interfaces import NotFound
from plone.namedfile.utils import set_headers, stream_data
import json
from five import grok

class ProducentDisplayForm(form.SchemaForm):
    schema = IProducent
    ignoreContext = False
    mode = 'display'

class ProducentFormView(FormWrapper):
    index = ViewPageTemplateFile('formwrapper.pt')

class AgreementDownload(BrowserView):
    def __call__(self):
        file_ = self.context.agreement

        if not file_:
            raise NotFound(self, 'smlouva-s-narodni-knihovnou.pdf', self.request)

        set_headers(file_, self.request.response, filename="smlouva-s-narodni-knihovnou.pdf")
        return stream_data(file_)

class GenerateAgreement(BrowserView):
    def __call__(self):
        with api.env.adopt_user(username="system"):
            wft = api.portal.get_tool('portal_workflow')
            wft.doActionFor(self.context,'generateAgreement')
            
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(dict(done = True))

class HasAgreement(BrowserView):
    def __call__(self):
        file_ = self.context.agreement
        widgetHTML = ""
        if file_:
            view = ProducentFormView(self.context, self.request)
            view = view.__of__(self.context)
            view.form_instance = ProducentDisplayForm(self.context, self.request)
            from lxml import html
            root = html.fromstring(view())
            widget = root.get_element_by_id('formfield-form-widgets-agreement')
            widgetHTML = html.tostring(widget).replace('/has-agreement/','/view/')

        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(dict(has_agreement = bool(file_),
                               agreement_widget_html = widgetHTML,
                           ))
        
