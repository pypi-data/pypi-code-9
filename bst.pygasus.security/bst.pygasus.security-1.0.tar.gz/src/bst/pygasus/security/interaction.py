from grokcore import component

from zope.security import management
from zope.component import getUtility
from zope.interface import implementer
from zope.security.interfaces import IParticipation
from zope.securitypolicy.zopepolicy import ZopeSecurityPolicy

from bst.pygasus.security import _
from bst.pygasus.security.principal import Principal
from bst.pygasus.security.interfaces import IAuthentication
from bst.pygasus.core.interfaces import IApplicationContext
from bst.pygasus.wsgi.events import IApplicationStartupEvent
from bst.pygasus.wsgi.interfaces import IApplicationSettings
from bst.pygasus.wsgi.events import IPreRequestProcessingEvent
from bst.pygasus.wsgi.events import IPostRequestProcessingEvent


ANONYMOUSE = Principal('bst.pygasus.anonymouse_user',
                       _('Anonymouse'),
                       _('Anonymouse user that is not logged in'))

AUTHENTICATED = Principal('bst.pygasus.authenticated_user',
                          _('Authenticated'),
                          _('Authenticated user that we know'))


@implementer(IParticipation)
class Participation(object):

    def __init__(self, principal):
        self.principal = principal
        # Note the interaction will be set by SecurityPolicy
        self.interaction = None


@component.subscribe(IApplicationSettings, IApplicationStartupEvent)
def set_policy_security(settings, event):
    management.setSecurityPolicy(ZopeSecurityPolicy)


# not finish at all, role and rights are not supported at the moment
"""
@component.subscribe(IApplicationContext, IPreRequestProcessingEvent)
def new_interaction(context, event):
    participations = list()
    principal = getUtility(IAuthentication).authenticate(event.request)
    if principal is not None:
        participations.append(Participation(principal))
        participations.append(Participation(AUTHENTICATED))
    else:
        participations.append(Participation(ANONYMOUSE))

    management.newInteraction(*participations)


@component.subscribe(IApplicationContext, IPostRequestProcessingEvent)
def end_interaction(context, event):
    management.endInteraction()
"""
