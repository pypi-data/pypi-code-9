# -*- coding: utf-8 -*-

from five import grok
from plone import api
from edeposit.user.producentfolder import IProducentFolder
from edeposit.user.producent import IProducent
from Products.CMFCore.interfaces import ISiteRoot
import json

class ProducentsSearch(grok.View):
    """A BrowserView to display the Producents listing on a Folder."""
    grok.context(ISiteRoot)
    #grok.require('zope2.View')  # what permission is needed for access
    grok.name('search-producents')  # on what URL will this view be available
    
    def update(self):
        # import pdb; pdb.set_trace()
        pass
    
    def render(self):
        portal_catalog = api.portal.get_tool(name='portal_catalog')
        brains = portal_catalog({'object_provides': IProducent.__identifier__})
        values = [ {'label': brain['Title'], 'value': brain['UID']} 
                   for brain in brains ]
        self.request.response.setHeader('Content-Type',
                                        'application/json; charset=utf-8')
        return json.dumps(values)
        

