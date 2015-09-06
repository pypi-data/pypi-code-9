# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

import unittest
import os.path
import sys
atLeastPython3 = sys.hexversion >= 0x03000000

import MockMockMock


class TestException(Exception):
    pass


class SystemCalls(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.mocks = MockMockMock.Engine()

    def testMockGloballyImportedFunction(self):
        original = os.path.exists
        m = self.mocks.replace("os.path.exists")
        m.expect("foo").andReturn(True)
        self.assertTrue(os.path.exists("foo"))
        self.mocks.tearDown()
        self.assertIs(os.path.exists, original)
        self.assertFalse(os.path.exists("foo"))

    def testMockLocallyImportedFunction(self):
        import subprocess
        original = subprocess.check_output
        m = self.mocks.replace("subprocess.check_output")
        m.expect(["foo", "bar"]).andReturn("baz\n")
        self.assertEqual(subprocess.check_output(["foo", "bar"]), "baz\n")
        self.mocks.tearDown()
        self.assertIs(subprocess.check_output, original)
        self.assertEqual(subprocess.check_output(["echo", "toto"]), b"toto\n" if atLeastPython3 else "toto\n")
