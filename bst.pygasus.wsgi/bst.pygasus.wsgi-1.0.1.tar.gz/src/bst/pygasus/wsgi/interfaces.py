from zope import interface


class IRootDispatcher(interface.Interface):
    """
    """

    def __init__(self, request, response):
        """
        """

    def run(self):
        """
        """


class IRequest(interface.Interface):
    """ Marker interface
    """


class IResponse(interface.Interface):
    """ Marker interface
    """


class IExceptionHandler(interface.Interface):
    """ Generic Exception Handler.
    """

    def __call__(self, context):
        """ return an Exception of type werkzeug.exceptions.HTTPException.
        """


class IApplicationSettings(interface.Interface):
    """ hold data that was passed form wsgi server
    """

    file = interface.Attribute('ini config file')
    here = interface.Attribute('absolute path to parts/etc')
