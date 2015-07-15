import pytest
from cybackup import dirwalker
import unittest
import os
import re

class DirwalkerFixt(unittest.TestCase):

    def setUp(self):
        self.source = "/home/cybernetics/"
        self.file_exceptions = ['~/saserrors.log','~/v.txt']
        self.dir_exceptions = ['~/olduser']

class DirwalkerTest(DirwalkerFixt):

    # test that the first excepted file does not appear
    def test_listing(self):
        lis = dirwalker.file_lister(self.source,
                file_exceptions=self.file_exceptions,
                dir_exceptions=self.dir_exceptions) 
        patt = re.compile(os.path.basename(self.file_exceptions[0]))
        for item in lis:
            print item
            self.assertEqual(patt.search(item), None,
                "Item: " + item)

    def test_dir_exceptions(self):
        lis = dirwalker.file_lister(self.source,
                file_exceptions=self.file_exceptions,
                dir_exceptions=self.dir_exceptions)
        patt = re.compile(os.path.basename(self.dir_exceptions[0]))
        for item in lis:
            self.assertEqual(patt.search(item), None,
                "Dir: " + item)

suite = unittest.TestLoader().loadTestsFromTestCase(DirwalkerTest)
unittest.TextTestRunner(verbosity=2).run(suite)
