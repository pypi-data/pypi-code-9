"""
Access icon themes.
"""

# Standard library modules.
import os
import glob
import warnings

# Third party modules.
from PySide.QtCore import QResource
from PySide.QtGui import QIcon

import pkg_resources

# Local modules.

# Globals and constants variables.

def init_resources():
    dirpath = pkg_resources.resource_filename(__name__, 'icons') #@UndefinedVariable
    for filepath in glob.glob(os.path.join(dirpath, '*.rcc')):
        if not QResource.registerResource(filepath):
            warnings.warn('Could not register rcc: %s filepath')
            continue
    QIcon.setThemeName('pyhmsa')

init_resources()

def getIcon(name):
    if not QIcon.hasThemeIcon(name):
        warnings.warn('Unknown icon theme: %s' % name)
        return QIcon()
    return QIcon.fromTheme(name)
