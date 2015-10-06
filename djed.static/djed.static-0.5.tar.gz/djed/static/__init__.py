import logging
import os
from collections import namedtuple

from zope.interface import Interface
from bowerstatic import (
    Bower,
    InjectorTween,
    PublisherTween,
)
from pyramid.interfaces import IApplicationCreated
from pyramid.path import AssetResolver
from pyramid.exceptions import ConfigurationError


log = logging.getLogger('djed.static')


BowerComponentsInfo = namedtuple('BowerComponentsInfo', 'name path')
BowerComponentInfo = namedtuple('BowerComponentInfo', 'path components_name')


class IBower(Interface):
    """ Bower interface
    """


class IBowerComponents(Interface):
    """ Bower components interface
    """


class IBowerComponent(Interface):
    """ Bower component interface for local components
    """


def bower_factory_from_settings(settings):
    prefix = settings.get('djed.static.prefix', 'djed.static.')

    bower = Bower()

    bower.initialized = False
    bower.publisher_signature = settings.get(
        prefix + 'publisher_signature', 'bowerstatic')
    bower.components_path = settings.get(
        prefix + 'components_path', None)
    bower.components_name = settings.get(
        prefix + 'components_name', 'components')

    return bower


def get_bower(request):
    registry = getattr(request, 'registry', None)
    if registry is None:
        registry = request
    return registry.getUtility(IBower)


def bowerstatic_tween_factory(handler, registry):
    bower = get_bower(registry)

    def bowerstatic_tween(request):
        injector_handler = InjectorTween(bower, handler)
        publisher_handler = PublisherTween(bower, injector_handler)

        return publisher_handler(request)

    return bowerstatic_tween


def add_bower_components(config, path, name=None):
    """
    """
    registry = config.registry
    resolver = AssetResolver()
    directory = resolver.resolve(path).abspath()

    if not os.path.isdir(directory):
        raise ConfigurationError(
            "Directory '{0}' does not exist".format(directory)
        )

    bower = get_bower(registry)

    if name is None:
        name = bower.components_name

    discr = ('djed:static', name)

    def register():
        info = BowerComponentsInfo(name, directory)
        registry.registerUtility(info, IBowerComponents, name=name)

    config.action(discr, register)


def add_bower_component(config, path, components_name=None):
    """
    """
    registry = config.registry
    resolver = AssetResolver()
    directory = resolver.resolve(path).abspath()

    if not os.path.isfile(os.path.join(directory, 'bower.json')):
        raise ConfigurationError(
            "Directory '{0}' does not contain 'bower.json' file"
            .format(directory)
        )

    bower = get_bower(registry)

    if components_name is None:
       components_name = bower.components_name

    discr = ('djed:static', directory, components_name)

    def register():
        info = BowerComponentInfo(directory, components_name)
        registry.registerUtility(info, IBowerComponent, name='-'.join(discr))

    config.action(discr, register)


def include(request, path_or_resource, components_name=None):
    """
    """
    registry = request.registry
    bower = get_bower(registry)

    if components_name is None:
        components_name = bower.components_name

    collection = bower._component_collections.get(components_name)

    if collection is None:
        raise ConfigurationError("Bower components '{0}' not found."
                                 .format(components_name))

    include = collection.includer(request.environ)
    include(path_or_resource)


def init_static(event):
    registry = event.app.registry
    bower = get_bower(registry)

    if not bower.initialized:
        log.info("Initialize static resources...")

        for name, info in registry.getUtilitiesFor(IBowerComponents):
            bower.components(info.name, info.path)

            log.info("Add static bower components '{0}': {1}"
                     .format(info.name, info.path))

        for name, info in registry.getUtilitiesFor(IBowerComponent):
            collection = bower._component_collections.get(info.components_name)

            if collection is None:
                raise ConfigurationError("Bower components '{0}' not found."
                            .format(info.components_name))

            component = collection.load_component(
                info.path, 'bower.json')

            collection.add(component)

            log.info("Add local bower component: {0}".format(info.path))

        bower.initialized = True


def includeme(config):
    bower = bower_factory_from_settings(config.registry.settings)
    config.registry.registerUtility(bower, IBower)

    config.add_tween('djed.static.bowerstatic_tween_factory')
    config.add_subscriber(init_static, IApplicationCreated)

    config.add_directive('add_bower_components', add_bower_components)
    config.add_directive('add_bower_component', add_bower_component)

    config.add_request_method(include, 'include')
    config.add_request_method(get_bower, 'get_bower')

    if bower.components_path is not None:
        config.add_bower_components(bower.components_path)
