from zope.interface import implementer
from zope.component.interfaces import IObjectEvent


class IPreRequestProcessingEvent(IObjectEvent):
    """ notify before the request is processed and
        before the transaction is beginning.
    """


@implementer(IPreRequestProcessingEvent)
class PreRequestProcessingEvent(object):
    def __init__(self, context, request):
        self.object = context
        self.request = request


class IPostRequestProcessingEvent(IObjectEvent):
    """ notify after request processing and after transaction commit.
    """


@implementer(IPostRequestProcessingEvent)
class PostRequestProcessingEvent(object):
    def __init__(self, context, request):
        self.object = context
        self.request = request


class IApplicationStartupEvent(IObjectEvent):
    """ notify one time at the application startup.
    """


@implementer(IApplicationStartupEvent)
class ApplicationStartupEvent(object):
    def __init__(self, settings):
        self.object = settings
