from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from twisted.internet.defer import inlineCallbacks
from twisted.internet import reactor
from autobahn.wamp import auth
from types import FunctionType
import traceback

class TestCase(ApplicationSession):

    WAMPCRA = u"wampcra"

    # Internal variables
    errors = 0
    failures = 0
    passes = 0
    tests = 0
    test_fail = False
    quiet = False
    test = False

    @classmethod
    def reset(cls):
        cls.errors = 0
        cls.failures = 0
        cls.passes = 0
        cls.tests = 0
        cls.test_fail = False

    #def onConnect(self):
        #if self.user is not None:
    #    if self.quiet is False:
    #        print "Attempting to join the realm '%s'" % self.realm
    #    self.join(unicode(self.realm), [self.WAMPCRA], unicode(self.user))

    #def onChallenge(self, challenge):
    #    if self.quiet is False:
    #        print "Received Auth Challenge"
    #    if challenge.method == self.WAMPCRA:
    #        signature = auth.compute_wcs(unicode(self.secret).encode('utf8'), challenge.extra['challenge'].encode('utf8'))
    #        return signature.decode('ascii')
    #    else:
    #        raise Exception("don't know how to handle authmethod {}".format(challenge.method))

    @inlineCallbacks
    def onJoin(self, details):

        for method_name in [x for x, y in self.__class__.__dict__.items() if type(y) == FunctionType]:

            if not method_name.startswith("test_"):
                continue

            self.__class__.tests += 1
            self.__class__.test_fail = False

            self.setUp()

            try:
                yield getattr(self, method_name)()
            except Exception, e:
                self._error(str(e))

            self.tearDown()

        if self.__class__.test is False:
            # Stops the reactor
            reactor.stop()

    @classmethod
    def connect(cls, url=None, realm=None, user=None, secret=None):
        print "Connecting to the url: '%s', realm: '%s'" % (url, realm)

        runner = ApplicationRunner(url=url, realm=realm)
        runner.run(cls)

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

    def _pass(self):
        self.__class__.passes += 1
        return True

    def _fail(self, message):
        # Can't exit since running in reactor so just suppress additional failures
        if self.__class__.test_fail is False:
            if self.quiet is False:
                stack = traceback.extract_stack()[-3:-1]
                path, line, test, instr = stack[0]
                print "\nFailure in %s: '%s'" % (test, message)
                print "    File: %s:%s" % (path, line)
                print "    Check: %s" % instr
            self.__class__.failures += 1
        self.__class__.test_fail = True
        return False

    def _error(self, message):
        if self.quiet is False:
            stack = traceback.extract_stack()[-3:-1]
            path, line, test, instr = stack[0]
            print "\nError in %s: '%s'" % (test, message)
            print "    File: %s:%s" % (path, line)
            print "    Check: %s" % instr
        self.__class__.errors += 1
        return False


def main(test_cases=None, url=None, realm=None, user=None, secret=None, quiet=False):
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

    TestCase.quiet = quiet

    if test_cases is None:
        test_cases = []

    if url is None:
        print "Connection 'url' must be defined."
        return 1

    if realm is None:
        print "Connection 'realm' must be defined."
        return 1

    errors = 0
    failures = 0
    passes = 0
    tests = 0

    # Iterate through the test cases
    for test_case in test_cases:

        # Ensure klass is the correct type
        if not issubclass(test_case, TestCase):
            raise Exception("The class '%s' is not a subclass of wamptest.TestCase" % test_case.__name__)

        # Initialize the test case
        test_case.reset()
        test_case.setUpClass()

        # Will exit when reactor is stopped in onJoin
        test_case.connect(url=url, realm=realm)

        # Get test suite results
        errors += test_case.errors
        failures += test_case.failures
        passes += test_case.passes
        tests += test_case.tests

        test_case.tearDownClass()

    # Print the results
    if quiet is False:
        heading = "\nResult:"
        if tests == 0:
            print heading, "UNKNOWN"
        elif (errors + failures) == 0:
            print heading, "PASSED"
        else:
            print heading, "FAILED"

        print "    Tests: %d" % tests
        print "    Passes: %d" % passes
        print "    Failures: %d" % failures
        print "    Errors: %d" % errors

    return errors + failures
