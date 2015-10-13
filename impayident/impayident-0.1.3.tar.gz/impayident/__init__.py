
"""
    Impay ident
    ~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 THE BEATPACKING COMPANY
    :license: MIT License
"""

import pkg_resources
VERSION = pkg_resources.resource_string('impayident', 'version.txt').strip()

from .api import cert, bill, sms
from .exc import *
from .const import *
