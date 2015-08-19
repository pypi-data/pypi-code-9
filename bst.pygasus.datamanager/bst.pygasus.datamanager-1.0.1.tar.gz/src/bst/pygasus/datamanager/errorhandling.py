import json
import traceback
import transaction

from bst.pygasus.core import ext
from bst.pygasus.datamanager.interfaces import IJSONExceptionHandler

from webob.exc import HTTPError


@ext.implementer(IJSONExceptionHandler)
class DefaultExceptionHandler(ext.Adapter):
    """ This adapter is for all exceptions types.
        The handler wrap the error message to a json
        response object and send it back to client.

        IN FUTURE WE SHOULD REMOVE THE ERROR MESSAGE FOR THE WEBUSER !!
    """

    ext.context(Exception)

    def __call__(self, request):
        self.request = request
        transaction.abort()
        print(traceback.format_exc())
        self.errorresponse(str(self.context), 500)

    def errorresponse(self, message, code):
        self.request.response.status_code = code
        self.request.response.write(json.dumps(dict(success=False,
                                                    message=message,
                                                    total=0,
                                                    data=list()),
                                    indent=' ' * 4))


@ext.implementer(IJSONExceptionHandler)
class DefaultHTTPExceptionHandler(DefaultExceptionHandler):
    """ This is a default adapter for HTTP errors. The client receive
        as json object with the a http error code.
    """
    ext.context(HTTPError)

    def __call__(self, request):
        self.request = request
        transaction.abort()
        self.errorresponse(str(self.context), self.context.code)
