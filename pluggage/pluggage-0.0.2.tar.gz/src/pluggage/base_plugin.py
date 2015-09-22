#!/usr/bin/env python
"""
_base_plugin_

Plugin base class that can be inherited to register
a class with a factory

"""

from .registry import get_factory
from .registry import PluggageMeta


class PluggagePlugin(object):
    __metaclass__ = PluggageMeta
    PLUGGAGE_FACTORY_NAME = 'abstract'
    PLUGGAGE_OBJECT_NAME = 'PluggagePlugin'

    def __init__(self):
        super(PluggagePlugin, self).__init__()
        self._factory_ref = None

    def _get_factory(self):
        """
        _get_factory_

        Helper method to get the appropriate factory
        for this DAO

        """
        if self._factory_ref is None:
            self._factory_ref = get_factory(self.PLUGGAGE_FACTORY_NAME)
        return self._factory_ref
