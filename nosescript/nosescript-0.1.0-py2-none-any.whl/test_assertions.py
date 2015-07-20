import os
import tempfile

import nose.config
import unittest.result

from .unit import NoseScriptUnit


class TestUnitPlugin(unittest.TestCase):
    """
    Minimal testing to ensure failures are raised properly, as other
    tests build on this.
    """
    def setUp(self):
        conf = nose.config.Config()
        self.plug = NoseScriptUnit()
        self.plug.configure(None, conf)
        self.plug.conf = conf

    def test_want_file(self):
        self.assertIsNone(self.plug.wantFile("foo.py"))
        self.assertIsNone(self.plug.wantFile("test_foo.py"))

        self.assertFalse(self.plug.wantFile("foo.js"))
        self.assertFalse(self.plug.wantFile("foo_test.js"))

        self.assertTrue(self.plug.wantFile("test_foo.js"))
        self.assertTrue(self.plug.wantFile("test.js"))
        self.assertTrue(self.plug.wantFile("Test.js"))

    def test_empty_load(self):
        sfile, sname = tempfile.mkstemp(suffix='.js')
        try:
            tests = self.plug.loadTestsFromFile(sname)
            self.assertIn(False, tests)
        finally:
            os.close(sfile)
            os.unlink(sname)

    def test_assert_false(self):
        sfile, sname = tempfile.mkstemp(suffix='.js')
        os.write(sfile, '''
QUnit.test('fail_me', function(assert) {assert.ok(false, 'noes')});''')
        try:
            tests = self.plug.loadTestsFromFile(sname)
            test = next(tests)
            self.assertTrue(test)

            error = test.test()
            self.assertIsNotNone(error)
            self.assertIsNotNone(error.name)
            self.assertEquals('AssertionError', error.name)
            self.assertIsNotNone(error.message)
            self.assertIsNotNone(error.stack)

            test_result = unittest.result.TestResult()
            self.assertFalse(test_result.errors)
            test.run(test_result)

            self.assertTrue(test_result.errors)
            _, trace = test_result.errors[0]
            self.assertRegexpMatches(trace, 'AssertionError: noes')
        finally:
            os.close(sfile)
            os.unlink(sname)

    def test_throws_fail(self):
        sfile, sname = tempfile.mkstemp(suffix='.js')
        os.write(sfile, '''
QUnit.test('fail_me', function(assert) {assert.throws(function(){})});''')
        try:
            tests = self.plug.loadTestsFromFile(sname)
            test = next(tests)
            self.assertTrue(test)

            error = test.test()
            self.assertIsNotNone(error)
            self.assertIsNotNone(error.name)
            self.assertEquals('AssertionError', error.name)
            self.assertIsNotNone(error.message)
            self.assertIsNotNone(error.stack)

            test_result = unittest.result.TestResult()
            self.assertFalse(test_result.errors)
            test.run(test_result)

            self.assertTrue(test_result.errors)
            _, trace = test_result.errors[0]
            self.assertRegexpMatches(trace, 'AssertionError:')
        finally:
            os.close(sfile)
            os.unlink(sname)

    def test_throws_pass(self):
        sfile, sname = tempfile.mkstemp(suffix='.js')
        os.write(sfile, '''
QUnit.test('fail_me', function(assert) {assert.throws(function(){
    throw {name: 'foo', message: 'kung'};
}, /kung/)});''')
        try:
            tests = self.plug.loadTestsFromFile(sname)
            test = next(tests)
            self.assertTrue(test)

            error = test.test()
            self.assertIsNone(error)
        finally:
            os.close(sfile)
            os.unlink(sname)
