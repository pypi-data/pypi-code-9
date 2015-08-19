import json
import gettext

import gettext

from grokcore import component

from bst.pygasus.wsgi.interfaces import IRequest
from bst.pygasus.wsgi.interfaces import IRootDispatcher
from bst.pygasus.core.interfaces import IApplicationContext

from zope.component import getUtility
from zope.component import queryUtility
from zope.i18n.interfaces import INegotiator
from zope.i18n.interfaces import ITranslationDomain
from zope.i18n.interfaces import IUserPreferredLanguages


@component.implementer(IRootDispatcher)
class I18nEntryPoint(component.MultiAdapter):
    """ Share translation strings from a .mo file as json to the
        application. Each domain can be reach separately.
    """

    component.name('i18n')
    component.adapts(IApplicationContext, IRequest)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        #TODO available language must be configurable!!!
        lang = getUtility(INegotiator).getLanguage(['de', 'fr'], self.request)
        self.request.response.content_type = 'application/json'

        self.request.path_info_pop()
        domain = self.request.path_info_pop()
        td = queryUtility(ITranslationDomain, name=domain)
        if td is None:
            return
        messages = dict()
        ret = dict(info=dict(Domain=domain,
                             Language=lang))
        for mofile in td.getCatalogsInfo().get(lang, []):
            with open(mofile, 'rb') as fp:
                # plural form is not supported at the moment, this
                # why zope.i18n missing this support.
                tr = gettext.GNUTranslations(fp)
                for k in tr._catalog.keys():
                    if k == '':
                        continue
                    messages[k] = tr._catalog[k]
        ret['messages'] = messages

        self.request.response.write(json.dumps(ret))


# https://grok-community-docs.readthedocs.org/en/latest/view_generation/i18n_of_your_app.html
class DefaultUserPreferredLanguages(component.Adapter):
    """ A very simple adapter that return the user preferred language
        with the browser information (Accept-Language).
    """

    component.context(IRequest)
    component.implements(IUserPreferredLanguages)

    def getPreferredLanguages(self):
        return self.context.accept_language
