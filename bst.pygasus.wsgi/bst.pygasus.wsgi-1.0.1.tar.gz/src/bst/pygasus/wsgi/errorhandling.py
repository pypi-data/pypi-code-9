import traceback
import transaction

from bst.pygasus.core import ext
from bst.pygasus.wsgi.interfaces import IExceptionHandler

from webob.exc import HTTPError
from webob.exc import HTTPInternalServerError


@ext.implementer(IExceptionHandler)
class DefaultExceptionHandler(ext.Adapter):
    """ This adapter is for all exceptions types.
        It recreate the exceptions and send it as
        InternalServerError.

        IN FUTURE WE SHOULD REMOVE THE ERROR MESSAGE FOR THE WEBUSER !!
    """

    ext.context(Exception)

    def __call__(self):
        transaction.abort()
        print(traceback.format_exc())
        return HTTPInternalServerError(str(self.context))


@ext.implementer(IExceptionHandler)
class DefaultHTTPExceptionHandler(ext.Adapter):
    """ This is a default adapter that do
        nothing else as return the same error.
    """
    ext.context(HTTPError)

    def __call__(self):
        transaction.abort()
        return self.context
