import configparser
from waitress import serve
from paste.deploy import loadapp

import zope.component.hooks
from zope.event import notify
from zope.interface import implementer
from zope.configuration import xmlconfig
from zope.configuration import config as zconfig

from bst.pygasus.wsgi.publisher import Publisher
from bst.pygasus.wsgi.events import ApplicationStartupEvent
from bst.pygasus.wsgi.interfaces import IApplicationSettings


@implementer(IApplicationSettings)
class ApplicationSettings(object):

    def __init__(self, global_conf):
        """ save the values that was
           passed by wsgi server.
        """
        self.file = global_conf['__file__']
        self.here = global_conf['here']


def make_app(global_conf={}, config='', debug=False):
    settings = ApplicationSettings(global_conf)
    zcmlconfigure(settings)
    notify(ApplicationStartupEvent(settings))
    return Publisher()


def make_debug(global_conf={}, config='', debug=False):
    """ do nothing else at the moment as the function make_app!!
    """

    return make_app(global_conf, config, debug)


def run(config=None):
    wsgi = loadapp('config:%s' % config)
    serve(wsgi)


def zcmlconfigure(settings):
    """ configuration for ZCML. The path to site.zcml must be
        written in the ini-file and defined in the section
        'zcml' as 'path'.
    """

    parser = configparser.ConfigParser()
    parser.read(settings.file)
    zcmlpath = parser.get('zcml', 'path')

    # Hook up custom component architecture calls
    zope.component.hooks.setHooks()

    # Load server-independent site config
    context = zconfig.ConfigurationMachine()
    xmlconfig.registerCommonDirectives(context)
    context = xmlconfig.file(zcmlpath, context=context, execute=True)

    return context
