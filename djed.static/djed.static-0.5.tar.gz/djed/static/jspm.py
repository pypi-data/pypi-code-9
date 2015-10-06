import logging
import json
from collections import namedtuple, OrderedDict

from zope.interface import Interface
from pyramid.path import AssetResolver

log = logging.getLogger('djed.static.jspm')


StaticApplication = namedtuple('StaticApplication', 'name asset_spec')

class IStaticApplication(Interface):
    """ Static application interfaces
    """


def jspm_tween_factory(handler, registry):

    content_types = set(['text/html', 'application/xhtml+xml'])


    def static_tween(request):
        response = handler(request)
        if response.content_type is None:
            return response
        if response.content_type.lower() not in content_types:
            return response

        app = registry.queryUtility(IStaticApplication)

        if app is None:
            return response

        text = response.text
        pos = text.find('</head>')
        if pos > -1:
            inclusions = []
            mods = request.jspm_imports

            static_url = request.static_url(app.asset_spec)

            inclusions.append('<script src="{0}{1}"></script>'.format(static_url, 'jspm_packages/system.js'))
            inclusions.append('<script>System.config({{"baseURL": "{0}"}})</script>'.format(static_url))
            inclusions.append('<script src="{0}{1}"></script>'.format(static_url, 'config.js'))
            inclusions.append('<script>{0}</script>'.format(''.join('System.import("{}");'.format(mod) for mod in mods)))

            response.text = '{0}{1}\n{2}'.format(
                text[:pos], '\n'.join(inclusions), text[pos:])

        return response

    return static_tween


def jspm_imports(request):
    return set()


def add_static_application(config, name, asset_spec):
    log.info("Add static application '{0}': {1}".format(name, asset_spec))

    #TODO: check if asset_spec endswith '/'

    config.add_static_view(name, asset_spec)
    
    app = StaticApplication(name, asset_spec)

    registry = config.registry
    registry.registerUtility(app, IStaticApplication)


def require(request, *mods):
    for mod in mods:
        request.jspm_imports.add(mod)


def includeme(config):
    config.add_tween('djed.static.jspm.jspm_tween_factory')

    config.add_directive('add_static_application', add_static_application)

    config.add_request_method(jspm_imports, 'jspm_imports', True, True)
    config.add_request_method(require, 'require')
