"""Unit tests for fibanez_social"""
# from fibanez_social.tests.test_facebook import *
# from fibanez_social.tests.test_twitter import *
# from fibanez_social.tests.test_linkdin import *


import unittest
import pkgutil
  
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(module_name).load_module(module_name)
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type) and issubclass(obj, unittest.case.TestCase):
            exec ('%s = obj' % obj.__name__)