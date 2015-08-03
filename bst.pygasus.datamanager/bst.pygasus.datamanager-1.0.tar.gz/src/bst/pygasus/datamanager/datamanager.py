import json
import sys
import traceback

from webob.exc import HTTPNotFound

from zope.component import getUtility
from zope.component import getMultiAdapter

from bst.pygasus.core import ext
from bst.pygasus.core.interfaces import IApplicationContext

from bst.pygasus.wsgi.interfaces import IRequest
from bst.pygasus.wsgi.interfaces import IRootDispatcher

from bst.pygasus.datamanager.interfaces import IModelHandler
from bst.pygasus.datamanager.interfaces import IModelTransformer
from bst.pygasus.datamanager.interfaces import IJSONExceptionHandler


@ext.implementer(IRootDispatcher)
class DataManagerEntryPoint(ext.MultiAdapter):
    """ manager all ajax request with CRUD options.
    """
    ext.name('data')
    ext.adapts(IApplicationContext, IRequest)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.request.response.content_type = 'application/javascript'

        try:
            self.request.path_info_pop()
            entity = self.request.path_info_pop()
            transformer = getUtility(IModelTransformer, entity)
            batch = transformer.model(self.request)
            results = list()
            total = 0
            for model in batch:
                handler = getMultiAdapter((model, self.request,), IModelHandler)
                result, subtotal = handler(model, batch)
                results += result
                total += subtotal
            data = transformer.json(results)
            self.successresponse('Data loaded from class %s' % model, data, total)
        except Exception as e:
            exceptionhandler = IJSONExceptionHandler(e)
            exceptionhandler(self.request)

    def successresponse(self, message, data, total):
        self.request.response.write(json.dumps(dict(success=True,
                                               message=message,
                                               total=total,
                                               data=data),
                                    indent=' ' * 4))
