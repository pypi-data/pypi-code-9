# -*- coding: utf-8 -*-
from zope.component import queryUtility
from zope.container.interfaces import IObjectAddedEvent, IObjectRemovedEvent,\
    IContainerModifiedEvent
from zope.interface import Interface
from plone import api
from edeposit.user import MessageFactory as _
from plone.dexterity.utils import createContentInContainer
import logging

logger = logging.getLogger('edeposit.content.handlers')

def addedProducentAdministrator(context, event):
    """
    When new administrator occurred, it is important to create user with the same username.
    """
    print "added producent administrator event handling"
    api.user.create(email=context.email, username=context.username, password=context.password)
    producent = context.aq_parent.aq_parent
    api.user.grant_roles(username=context.username,  
                         obj=producent,
                         roles=('E-Deposit: Producent Administrator',
                                'E-Deposit: Producent Editor',
                                'Reviewer','Editor','Contributor','Reader')
    )
    api.group.add_user(groupname="Producent Administrators",
                       username=context.username,
    )
    api.group.add_user(groupname="Producent Contributors",
                       username=context.username,
    )
    api.group.add_user(groupname="Producent Editors",
                       username=context.username,
    )
    producent.reindexObject()
    pass

def addedProducentEditor(context, event):
    """
    When new editor occurred, it is important to create user with the same username.
    """
    print "added producent editor event handling"
    api.user.create(email=context.email, username=context.username, password=context.password)
    producent = context.aq_parent.aq_parent
    api.user.grant_roles(username=context.username,  
                         obj=producent,
                         roles=('E-Deposit: Producent Editor',
                                'Reader')
                     )
    api.group.add_user(groupname="Producent Editors",
                       username=context.username,
                   )
    api.group.add_user(groupname="Producent Contributors",
                       username=context.username,
                   )
    epublications = producent['epublications']
    api.user.grant_roles(username=context.username,
                         obj = epublications,
                         roles=('E-Deposit: Producent Editor','Contributor')
                     )
    producent.reindexObject()
    pass

def added(context,event):
    """When an object is added, create folder for registration of ePublications
    """
    # tool = api.portal.get_tool('translation_service')
    # title = tool.translate(msgid=u"Registration of ePublications", 
    #                        domain='edeposit.user',
    #                        context=context, 
    #                        target_language='cs')
    context.invokeFactory('edeposit.content.epublicationfolder','epublications', title=u"Ohlášené ePublikace")
    context.invokeFactory('edeposit.content.eperiodicalfolder','eperiodicals', title=u"Ohlášená ePeriodika")
    context.invokeFactory('edeposit.content.bookfolder','books', title=u"Ohlášené tištěné knihy")
    # context.invokeFactory('edeposit.user.producentadministratorfolder','producent-administrators',title=u"Administrátoři")
    # context.invokeFactory('edeposit.user.producenteditorfolder','producent-editors',title=u"Editoři")
    # context.invokeFactory('edeposit.content.originalfilecontributingrequestsfolder',
    #                       'originalfile-contributing',
    #                       title=u"Odevzdané dokumenty")
