from cgi import escape
from datetime import date
from urllib import unquote

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

import plone.app.content
import plone.app.layout
from plone.app.layout.viewlets import common as base
from zope.publisher.interfaces import NotFound
from plone.namedfile.utils import set_headers, stream_data
import json

class DownloadButton(base.ViewletBase):
    index = ViewPageTemplateFile('downloadbutton.pt')

class AgreementDownload(BrowserView):
    def __call__(self):
        file_ = self.context.agreement

        if not file_:
            raise NotFound(self, 'smlouva.pdf', self.request)

        set_headers(file_, self.request.response, filename="smlouva.pdf")
        return stream_data(file_)

class HasAgreement(BrowserView):
    def __call__(self):
        file_ = self.context.agreement
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(dict(has_agreement = bool(file_)))
