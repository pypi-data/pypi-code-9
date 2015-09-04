# coding: utf-8
"""
This is a module that handle a import of rh data.
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from future import standard_library
standard_library.install_aliases()
from builtins import *
from rh.models import *
from .data_importer import BaseImporter


class RHImporter(BaseImporter):
    pass
