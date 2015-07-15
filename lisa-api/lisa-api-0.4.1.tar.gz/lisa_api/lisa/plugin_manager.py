from stevedore import extension
from lisa_api.lisa.logger import logger


class PluginManager(object):
    __instance = None

    def __new__(cls):
        if PluginManager.__instance is None:
            PluginManager.__instance = object.__new__(cls)
        return PluginManager.__instance

    def __init__(self):
        self.mgr = None
        self.plugins = []
        self.django_plugins = []
        self.load_plugins()

    def load_plugins(self):
        self.mgr = extension.ExtensionManager(
            namespace='lisa.api.plugins',
            invoke_on_load=True,
            verify_requirements=True
        )
        self.plugins = self.mgr.names()
        for plugin in self.plugins:
            self.django_plugins.append('lisa_plugins_%s' % plugin)
        logger.info("Loaded plugins : %s" % self.plugins)

    def load_intents(self):
        if self.plugins:
            logger.info("Adding intents to database")
            try:
                self.mgr.map(lambda ext: (ext.name, ext.obj.add_intents()))
            except RuntimeError:
                logger.info("There was a problem loading plugins intents")
        else:
            logger.info("There is no plugin loaded")

    def get_version(self, plugin_name):
        if self.plugins:
            try:
                version = self.mgr.map(lambda ext: (ext.name, ext.obj.get_version()))
                for plugin in version:
                    if plugin_name == plugin[0]:
                        return plugin[1]
            except RuntimeError:
                logger.info("There was a problem loading plugins")
        else:
            logger.info("There is no plugin loaded")
