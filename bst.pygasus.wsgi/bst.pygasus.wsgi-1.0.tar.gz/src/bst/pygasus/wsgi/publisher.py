import transaction

from bst.pygasus.wsgi import events
from bst.pygasus.wsgi import interfaces
from bst.pygasus.wsgi.http import Request
from bst.pygasus.wsgi.http import Response
from bst.pygasus.core.interfaces import IApplicationContext
from bst.pygasus.core.interfaces import DEFAULT_EXTJS_APPLICATION

from zope.event import notify
from zope.component import queryUtility
from zope.component.hooks import setSite
from zope.component import queryMultiAdapter

from webob.exc import HTTPNotFound


class Publisher(object):

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def dispatch_request(self, request):
        request.response = Response()

        appname = request.path_info_peek()
        if not appname:
            appname = DEFAULT_EXTJS_APPLICATION
        context = queryUtility(IApplicationContext, name=appname)

        if context is None:
            raise NotImplementedError('No utility found for IApplicationContext. Application can not be started.')
        # hooks context to local site manager
        setSite(context)
        request.path_info_pop()
        dispatchname = request.path_info_peek()

        if dispatchname is None:
            dispatchname = 'index'

        dispatcher = queryMultiAdapter((context, request), interfaces.IRootDispatcher, dispatchname)
        try:
            if dispatcher is None:
                raise HTTPNotFound('%s was not found' % dispatchname)
            notify(events.PreRequestProcessingEvent(context, request))
            transaction.begin()
            dispatcher()
            transaction.commit()
            notify(events.PostRequestProcessingEvent(context, request))

            return request.response
        except Exception as e:
            handler = interfaces.IExceptionHandler(e)
            return handler()
        #except RetryException as e:
        #
        # if we begin to work with a sql database we properly
        # need to work with a RetryException. Show zope.publisher as
        # example and implement it here,
