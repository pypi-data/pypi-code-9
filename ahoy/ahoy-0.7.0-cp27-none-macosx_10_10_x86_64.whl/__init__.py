# -*- coding: utf-8 -*-

from ahoy._version import get_versions

__author__ = 'Elliot Marsden'
__email__ = 'elliot.marsden@gmail.com'
__version__ = get_versions()['version']

del get_versions

from ahoy import directions
from ahoy import positions
from ahoy import measurers
from ahoy import rudders
from ahoy import swimmers
from ahoy import agents
from ahoy import ships
from ahoy import stime
