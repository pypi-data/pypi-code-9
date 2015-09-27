from pyramid.view import view_config

from pyramid.httpexceptions import (
    HTTPSeeOther,
    HTTPBadRequest,
    HTTPNotFound
)


@view_config(route_name='redirect')
def redirect(request):
    uri = request.host_url + '/' + request.matchdict['uri']
    redirect = request.uri_handler.handle(uri, request)
    if not redirect:
        raise HTTPNotFound()
    return HTTPSeeOther(redirect)


@view_config(route_name='handle')
def handle(request):
    uri = request.params.get('uri', None)
    if not uri:
        raise HTTPBadRequest('Please include a URI parameter.')
    redirect = request.uri_handler.handle(uri, request)
    if not redirect:
        raise HTTPNotFound('Unknown URI.')
    return HTTPSeeOther(redirect)
