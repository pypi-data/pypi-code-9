"""
Fix of QSettings
"""

# Standard library modules.

# Third party modules.
from PySide.QtCore import QSettings

import six

import matplotlib.colors as colors

# Local modules.

# Globals and constants variables.

class Settings(QSettings):

    def valueBool(self, key, default):
        value = self.value(key, default)
        if isinstance(value, six.string_types):
            value = True if value.lower() == 'true' else False
        return value

    def setValueColor(self, key, value):
        r, g, b = colors.colorConverter.to_rgb(value)
        self.setValue(key, ';'.join(map(str, [r, g, b])))

    def valueColor(self, key, default):
        value = self.value(key, default)
        if ';' in value:
            r, g, b = map(float, value.split(';'))
        else:
            r, g, b = colors.colorConverter.to_rgb(value)
        return r, g, b
