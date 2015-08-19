import webob
from bst.pygasus.core import ext
from bst.pygasus.wsgi import interfaces


@ext.implementer(interfaces.IRequest)
class Request(webob.Request):
    pass


@ext.implementer(interfaces.IResponse)
class Response(webob.Response):
    pass
