import unittest
# import unittest2 as unittest # for versions of python < 2.7

"""
        Method                  Checks that
self.assertEqual(a, b)           a == b   
self.assertNotEqual(a, b)        a != b   
self.assertTrue(x)               bool(x) is True  
self.assertFalse(x)              bool(x) is False     
self.assertIs(a, b)              a is b
self.assertIsNot(a, b)           a is not b
self.assertIsNone(x)             x is None 
self.assertIsNotNone(x)          x is not None 
self.assertIn(a, b)              a in b
self.assertNotIn(a, b)           a not in b
self.assertIsInstance(a, b)      isinstance(a, b)  
self.assertNotIsInstance(a, b)   not isinstance(a, b)  

See:
      https://docs.python.org/2/library/unittest.html
         or
      https://docs.python.org/dev/library/unittest.html
for more assert options
"""

import sys, os
here = os.path.abspath(os.path.dirname(__file__))
up_one = os.path.split( here )[0]  # Needed to find tk_nosy development version
if here not in sys.path[:3]:
    sys.path.insert(0, here)
if up_one not in sys.path[:3]:
    sys.path.insert(0, up_one)

from tk_nosy.main_gui import Tk_Nosy
from tk_nosy.pyterps import PyInterpsOnSys
from tkinter import Tk
from tkinter import Toplevel


class MyTest(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.myclass = PyInterpsOnSys()

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del( self.myclass )

    def test_should_always_pass_cleanly(self):
        """Should always pass cleanly."""
        pass

    def test_myclass_existence(self):
        """Check that myclass exists"""
        result = self.myclass

        # See if the self.myclass object exists
        self.assertTrue(result)
        
    #def test_Tk_creation(self):
    #    """Check that a Tk_Nosy object can be created"""
    #    root = Tk()
    #    result = Tk_Nosy(root)

    #    # See if the Tk_Nosy object exists
    #    self.assertTrue(result)


if __name__ == '__main__':
    # Can test just this file from command prompt
    #  or it can be part of test discovery from nose, unittest, pytest, etc.
    unittest.main()

