"""this module implement api to controller for transaction.

"""

import threading
import logging
import tingyun.api.settings
import tingyun.api.tracert.controller

_logger = logging.getLogger(__name__)


class ApplicationProxy(object):
    _lock = threading.Lock()
    _instances = {}

    def __init__(self, controller, name):
        self._app_name = name
        self.enabled = True

        if not controller:
            controller = tingyun.api.tracert.controller.controller_instance()
            _logger.debug("init application with new controller")

        self._controller = controller

    @staticmethod
    def singleton_instance(name):
        """one application according to name
        """
        if not name:
            name = tingyun.api.settings.global_settings().app_name

        controller = tingyun.api.tracert.controller.controller_instance()
        instance = ApplicationProxy._instances.get(name, None)
        
        if not instance:
            with ApplicationProxy._lock:
                instance = ApplicationProxy._instances.get(name, None)
                if not instance:
                    instance = ApplicationProxy(controller, name)
                    ApplicationProxy._instances[name] = instance

                    _logger.info("new application with name: %s", name)

        return instance

    @property
    def global_settings(self):
        """get the global settings or server settings
        :return:
        """
        global_settings = self._controller.global_settings()

        return global_settings

    @property
    def settings(self):
        """
        :return:
        """
        return self._controller.application_settings(self._app_name)

    def activate(self, timeout=None):
        """
        :param timeout:
        :return:
        """
        self._controller.active_application(self._app_name)
        
    def record_transaction(self, transaction_node):
        """
        """
        self._controller.record_transaction(self._app_name, transaction_node)


def proxy_instance(name=None):
    return ApplicationProxy.singleton_instance(name)
