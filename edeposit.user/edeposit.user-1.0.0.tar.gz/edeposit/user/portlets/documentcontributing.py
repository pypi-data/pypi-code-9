from zope.interface import Interface
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import re
from plone import api
import os.path

from edeposit.user import MessageFactory as _
import itertools
from edeposit.user.producent import IProducent
from edeposit.content.epublicationfolder import IePublicationFolder
from edeposit.content.eperiodicalfolder import IePeriodicalFolder
from edeposit.content.bookfolder import IBookFolder

class IDocumentContributing(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    # TODO: Add any zope.schema fields here to capture portlet configuration
    # information. Alternatively, if there are no settings, leave this as an
    # empty interface - see also notes around the add form and edit form
    # below.

    # some_field = schema.TextLine(title=_(u"Some field"),
    #                              description=_(u"A field to use"),
    #                              required=True)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IDocumentContributing)

    # TODO: Set default values for the configurable parameters here

    # some_field = u""

    # TODO: Add keyword parameters for configurable parameters here
    # def __init__(self, some_field=u''):
    #    self.some_field = some_field

    def __init__(self):
        pass

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return _(u"E-Deposit: Registering of any eContent")


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('documentcontributing.pt')

    def member(self):
        return api.user.get_current()

    def assignedProducents(self):
        user = api.user.get_current()
        username = user.getUserName()
        portal_catalog = api.portal.get_tool(name='portal_catalog')
        brains = portal_catalog({'object_provides': IProducent.__identifier__})

        def userIsAssigned(brain):
            user_local_roles = api.user.get_roles(obj=brain.getObject())
            return 'E-Deposit: Producent Administrator' in user_local_roles \
                or 'E-Deposit: Producent Editor' in user_local_roles \
                or 'E-Deposit: Producent Contributor' in user_local_roles

        producentInfos = [ {'path': brain.getPath(), 'UID': brain['UID'] , 'title': brain['Title'] } 
                           for brain in (brains or []) if userIsAssigned(brain)
                           ]
        
        #/edeposit/producenti/jeste-jeden-od-anonyma/epublications/++add++edeposit.content.epublication
        def getRegisteringPaths(producentPath):
            brains = portal_catalog({'object_provides': [IePublicationFolder.__identifier__,
                                                         IePeriodicalFolder.__identifier__,
                                                         IBookFolder.__identifier__
                                                     ],
                                     'path': producentPath 
                                     })
            def getRegistrationPath(brain):
                path = brain.getPath()
                portal_type = brain.portal_type
                item_portal_type = re.sub("folder$","",portal_type)
                url = os.path.join(path,"++add++%s"% (item_portal_type,))
                return {'desc': brain['Title'], 'href': url}
            
            return map(getRegistrationPath, brains or [])
        
        return [ {'name': producentInfo['title'],         
                  'path': producentInfo['path'],
                  'links': getRegisteringPaths(producentInfo['path'])} for
                 producentInfo in (producentInfos or [])]
        
# NOTE: If this portlet does not have any configurable parameters, you can
# inherit from NullAddForm and remove the form_fields variable.

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IDocumentContributing)

    def create(self, data):
        return Assignment(**data)

