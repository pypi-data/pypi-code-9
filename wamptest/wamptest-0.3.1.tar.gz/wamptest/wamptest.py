from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor
from autobahn.wamp import auth
from types import FunctionType
import traceback
import sys
from contextlib import contextmanager


class TestRunner(object):

    def __init__(self, test_cases, url, realm, quiet=False, test=False, user=None, secret=None):
        self.total_tests = 0
        self.total_errors = 0
        self.total_failures = 0
        self.total_passes = 0

        self.quiet = quiet
        self.test = test
        self.test_fail = False

        self.test_cases = test_cases
        self.test_case_number = 0
        self.url = url
        self.realm = realm

        self.auth_user = user
        self.auth_secret = secret

    def run(self):
        if len(self.test_cases) > 0:
            test_case = self.test_cases[0]
            test_case.connect(url=self.url, realm=self.realm, test_runner=self)

            if self.test is False:
                reactor.run()

    def report_test_results(self, tests, errors, failures, passes):
        self.total_tests += tests
        self.total_errors += errors
        self.total_failures += failures
        self.total_passes += passes

        self.test_case_number += 1
        if self.test_case_number < len(self.test_cases):
            test_case = self.test_cases[self.test_case_number]
            test_case.connect(url=self.url, realm=self.realm, test_runner=self)
        elif self.test is False:
            reactor.stop()


class TestCase(ApplicationSession):

    WAMPCRA = u"wampcra"

    test_runner = None
    quiet = False

    def is_quiet(self):
        test_runner = self.get_test_runner()
        if test_runner is not None:
            return test_runner.quiet or self.__class__.quiet
        else:
            return self.__class__.quiet

    def get_test_runner(self):
        return self.__class__.test_runner

    def __init__(self, config):
        super(TestCase, self).__init__(config)

        self.errors = 0
        self.failures = 0
        self.tests = 0
        self.passes = 0

        self.test_fail = False

    def reset(self):
        self.errors = 0
        self.failures = 0
        self.passes = 0
        self.tests = 0

        self.test_fail = False

    def onConnect(self):
        if self.get_test_runner().auth_user is not None:
            self.join(self.config.realm, [u"wampcra"], unicode(self.get_test_runner().auth_user))
        else:
            super(TestCase, self).onConnect()

    def onChallenge(self, challenge):
        if challenge.method == u"wampcra":
            signature = auth.compute_wcs(
                unicode(self.get_test_runner().auth_secret).encode('utf8'),
                challenge.extra['challenge'].encode('utf8')
            )
            return signature.decode('ascii')
        else:
            raise Exception("don't know how to handle authmethod {}".format(challenge.method))

    @inlineCallbacks
    def onJoin(self, details):

        # Setup the class
        self.reset()
        self.__class__.setUpClass()

        for method_name in [x for x, y in self.__class__.__dict__.items() if type(y) == FunctionType]:

            if not method_name.startswith("test_"):
                continue

            self.tests += 1
            self.test_fail = False

            self.setUp()

            try:
                yield getattr(self, method_name)()
            except BaseException, e:
                self._error(str(e))

            self.tearDown()

        # Teardown the class
        self.__class__.tearDownClass()

        # Report Done
        self.get_test_runner().report_test_results(
            tests=self.tests,
            errors=self.errors,
            failures=self.failures,
            passes=self.passes
        )

        if self.get_test_runner().test is False:
            # Disconnect
            print "Disconnecting from the Session"
            self.disconnect()

    @classmethod
    def connect(cls, url=None, realm=None, test_runner=None, user=None, secret=None):
        print "Connecting to the url: '%s', realm: '%s'" % (url, realm)

        cls.test_runner = test_runner

        runner = ApplicationRunner(url=url, realm=realm)
        runner.run(cls, start_reactor=False)

    @classmethod
    def setUpClass(cls):
        """
        Run once before the test suite is run
        :return: Nothing
        """
        pass

    @classmethod
    def tearDownClass(cls):
        """
        Run once after the test suite is run
        :return: Nothing
        """
        pass

    def setUp(self):
        """
        Run once before each test is run
        :return: Nothing
        """
        pass

    def tearDown(self):
        """
        Run once after each test is run
        :return: Nothing
        """
        pass

    def assertEqual(self, a, b, msg=None):
        """
        Asserts that a value is equal to another value
        :param a: The value
        :param b: The other value
        :param msg: Custom message on failure
        :return: True is the assertion passed
        """
        if a != b:
            if msg is None:
                msg = "Expected '%s' to equal '%s'" % (a, b)
            return self._fail(msg)
        else:
            return self._pass()

    def assertNotEqual(self, a, b, msg=None):
        """
        Asserts that a value is equal to another value
        :param a: The value
        :param b: The other value
        :param msg: Custom message on failure
        :return: True is the assertion passed
        """
        if a == b:
            if msg is None:
                msg = "Expected '%s' to not equal '%s'" % (a, b)
            return self._fail(msg)
        else:
            return self._pass()

    def assertIsNone(self, a, msg=None):
        """
        Asserts that a value is None
        :param a: The value
        :param msg: Custom message on failure
        :return: True is the assertion passed
        """
        if a is not None:
            if msg is None:
                msg = "'%s' should be 'None'" % a
            return self._fail(msg)
        else:
            return self._pass()

    def assertIsNotNone(self, a, msg=None):
        """
        Asserts that a value is not None
        :param a: The value
        :param msg: Custom message on failure
        :return: True is the assertion passed
        """
        if a is None:
            if msg is None:
                msg = "'%s' should not be 'None'" % a
            return self._fail(msg)
        else:
            return self._pass()

    def assertTrue(self, a, msg=None):
        """
        Asserts that a value is True
        :param a: The value
        :param msg: Custom message on failure
        :return: True is the assertion passed
        """
        if a is not True:
            if msg is None:
                msg = "'%s' should be 'True'" % a
            return self._fail(msg)
        else:
            return self._pass()

    def assertFalse(self, a, msg=None):
        """
        Asserts that a value is False
        :param a: The value
        :param msg: Custom message on failure
        :return: True is the assertion passed
        """
        if a is not False:
            if msg is None:
                msg = "'%s' should be 'False'" % a
            return self._fail(msg)
        else:
            return self._pass()

    def assertGreater(self, a, b, msg=None):
        """
        Asserts that a value is greater than another value
        :param a: The value
        :param b: The other value
        :param msg: Custom message on failure
        :return: True is the assertion passed
        """
        if not a > b:
            if msg is None:
                msg = "'%s' should be greater than '%s'" % (a, b)
            return self._fail(msg)
        else:
            return self._pass()

    def assertGreaterEqual(self, a, b, msg=None):
        """
        Asserts that a value is greater than or equal to another value
        :param a: The value
        :param b: The other value
        :param msg: Custom message on failure
        :return: True is the assertion passed
        """
        if not a >= b:
            if msg is None:
                msg = "'%s' should be greater than or equal to '%s'" % (a, b)
            return self._fail(msg)
        else:
            return self._pass()

    def assertLess(self, a, b, msg=None):
        """
        Asserts that a value is less than another value
        :param a: The value
        :param b: The other value
        :param msg: Custom message on failure
        :return: True is the assertion passed
        """
        if not a < b:
            if msg is None:
                msg = "'%s' should be less than '%s'" % (a, b)
            return self._fail(msg)
        else:
            return self._pass()

    def assertLessEqual(self, a, b, msg=None):
        """
        Asserts that a value is less than or equal to another value
        :param a: The value
        :param b: The other value
        :param msg: Custom message on failure
        :return: True is the assertion passed
        """
        if not a <= b:
            if msg is None:
                msg = "'%s' should be less than or equal to '%s'" % (a, b)
            return self._fail(msg)
        else:
            return self._pass()

    @contextmanager
    def assertRaises(self, exception_class, msg=None):
        """
        Asserts that a block of code raises an exception
        :param exception_class: The type of class expected
        :param msg: Custom message on failure
        """
        success = False
        exc = None
        try:
            yield exception_class
        except BaseException, e:
            print e
            exc = e

        if exc is not None:
            if issubclass(exc.__class__, exception_class):
                success = True

        if success is False:
            if msg is None:
                msg = "method should raise exception of type '%s'" % exception_class.__name__
            self._fail(msg)
        else:
            self._pass()

    def _pass(self):
        self.passes += 1
        return True

    def _fail(self, message):
        # Can't exit since running in reactor so just suppress additional failures
        if self.test_fail is False:
            if self.is_quiet() is False:
                stack = traceback.extract_stack()[-3:-1]
                path, line, test, instr = stack[0]
                print "\nFailure in %s: '%s'" % (test, message)
                print "    File: %s:%s" % (path, line)
                print "    Check: %s" % instr
            self.failures += 1
        self.test_fail = True
        return False

    def _error(self, message):
        if self.is_quiet() is False:
            stack = traceback.extract_stack()[-3:-1]
            path, line, test, instr = stack[0]
            print "\nError in %s: '%s'" % (test, message)
            print "    File: %s:%s" % (path, line)
            print "    Check: %s" % instr
        self.errors += 1
        return False


def main(test_cases=None, url=None, realm=None, user=None, secret=None, quiet=False, test=False):
    """
    Runs the test cases.  Example of use is as follows

    import wamptest
    from twisted.internet.defer import inlineCallbacks
    from autobahn.twisted.util import sleep

    class ExampleTestCase(wamptest.TestCase):

        @inlineCallbacks
        def test_1(self):
            result = yield self.call("com.example.add", 1, 2)
            self.assertEqual(3, result)

        def receive_update(self, update=None):
            self.update = update

        @inlineCallbacks
        def test_2(self):
            self.subscribe(self.receive_update, topic="com.example.update")

            # Trigger update

            yield sleep(2)

            self.assertEqual("test", self.update)

    result = wamptest.main(
        test_cases=[ExampleTestCase],
        url="ws://router.example.com",
        realm="realm1"
    )

    exit(result)

    :param test_cases: Array of the test cases
    :param url: The url of the router
    :param realm: The realm of the router
    :param user: The user to authenticate as (wampcra)
    :param secret: The secret for the user (wampcra)
    :param quiet: True if silencing logging
    :return: number of total errors and failures
    """

    if test_cases is None:
        test_cases = []

    if url is None:
        print "Connection 'url' must be defined."
        return 1

    if realm is None:
        print "Connection 'realm' must be defined."
        return 1

    # Run the tests
    test_runner = TestRunner(test_cases, url, realm, quiet=quiet, test=test, user=user, secret=secret)
    test_runner.run()

    # Print the results
    if quiet is False:
        heading = "\nResult:"
        if test_runner.total_tests == 0:
            print >> sys.stderr, heading, "UNKNOWN"
        elif (test_runner.total_errors + test_runner.total_failures) == 0:
            print >> sys.stderr, heading, "PASSED"
        else:
            print >> sys.stderr, heading, "FAILED"

        print >> sys.stderr, "    Tests: %d" % test_runner.total_tests
        print >> sys.stderr, "    Passes: %d" % test_runner.total_passes
        print >> sys.stderr, "    Failures: %d" % test_runner.total_failures
        print >> sys.stderr, "    Errors: %d" % test_runner.total_errors

    sys.stdout.flush()

    return test_runner.total_errors + test_runner.total_failures
