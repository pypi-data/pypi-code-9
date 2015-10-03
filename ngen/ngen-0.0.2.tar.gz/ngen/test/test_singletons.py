from twisted.trial.unittest import TestCase
from twisted.internet import reactor, defer

from ngen.singletons import Singleton, SingletonPrime, lock
from ngen.utils import threaded

import mock
import time


class Catalog(Singleton):

    def setUp(self):
        self.registry = {}


class Mixin(object):

    def hello(self):
        return 'sup ' + self.name if hasattr(self, 'name') else 'nope'


class Frank(Catalog, Mixin):
    pass


class SingletonTests(TestCase):

    def setUp(self):
        # clears out the singleton instance
        Singleton._instance = None

    def test_Singleton_is_a_singleton(self):
        instance_a = Singleton()
        instance_b = Singleton()

        self.assertTrue(instance_a is instance_b)

    def test_setUp_is_run_on_initialization(self):
        with mock.patch('ngen.singletons.Singleton.setUp') as setUp:
            Singleton()
            self.assertTrue(setUp.called)


class SingletonInheritanceTests(TestCase):

    def setUp(self):
        self.singleton = Singleton()
        self.catalog = Catalog()
        self.frank = Frank()

    def tearDown(self):
        # clear out the singletons
        self.singleton._instance = None
        self.catalog._instance = None
        self.frank._instance = None

    def test_not_effected_by_instantiating_Singleton_first(self):
        self.assertTrue(self.catalog is not self.singleton)

    def test_catalog_has_registry(self):
        self.assertTrue(hasattr(self.catalog, 'registry'))

    def test_reset_works(self):
        self.catalog.registry['food'] = 'bar'
        self.catalog.reset()
        self.assertEqual(self.catalog.registry, {})

    def test_mixins_work_with_attr_assignment(self):
        self.frank.name = 'sam'
        self.assertEqual(self.frank.hello(), 'sup sam')

    def test_mixins_work(self):
        self.assertEqual(self.frank.hello(), 'nope')


class StillSingletonPrime(SingletonPrime):

    def setUp(self):
        self.food = 'bar'


class SingletonPrimeTests(TestCase):

    def setUp(self):
        SingletonPrime._clear()

    def test_SingletonPrime_is_a_singleton(self):
        instance_a = SingletonPrime()
        instance_b = SingletonPrime()

        self.assertTrue(instance_a is instance_b)

    def test_inheritance_references_the_object_of_the_first_class_init(self):
        a = SingletonPrime()
        b = StillSingletonPrime()
        self.assertTrue(a is b)

    def test_inheritance_breaks(self):
        SingletonPrime()
        b = StillSingletonPrime()
        self.assertRaises(AttributeError, getattr, b, 'food')

    def test_inheritance_works_when_instantiation_is_clean(self):
        b = StillSingletonPrime()
        self.assertEqual(b.food, 'bar')


EXPECTED = range(300)


class ThreadNeverSafeSingleton(Singleton):

    def setUp(self):
        self.data = []
        self.counter = 0
        self.container = [0 for _ in EXPECTED]

    def add(self, val):
        """
            appending to a list and assuming that the order will be the same
            will not be safe even if the `lock` method is used.
        """
        self.data.append(val)

    def set(self, val):
        """
            set is another example of how to not use `lock` i.e. where it will
            have no effect.
        """
        try:
            self.container[self.counter] = val
        except IndexError:
            # N.B. can run into this for some reason
            # import ipdb; ipdb.set_trace()
            pass

    def inc(self):
        self.counter += 1


class ThreadAddNotSafeSingleton(ThreadNeverSafeSingleton):

    @lock
    def add(self, val):
        self.data.append(val)


class ThreadSetNotSafeSingleton(ThreadAddNotSafeSingleton):

    @lock
    def set(self, val):
        super(ThreadSetNotSafeSingleton, self).set(val)

    @lock
    def inc(self):
        self.counter += 1


class ThreadedSingleton(Singleton):

    def setUp(self):
        self.counter = 0

    @threaded
    def acquire(self):
        self.lock.acquire()

    @lock
    def wont_ever_run(self):
        time.sleep(0.05)
        self.counter = 1


class SingletonThreadSafetyTests(TestCase):

    def setUp(self):
        self.setnotsafe = ThreadSetNotSafeSingleton()
        self.addnotsafe = ThreadAddNotSafeSingleton()
        self.neversafe = ThreadNeverSafeSingleton()

    def tearDown(self):
        self.setnotsafe._instance = None
        self.addnotsafe._instance = None
        self.neversafe._instance = None

    def _do_junk(self, result, ref):
        for idx in EXPECTED:
            reactor.callInThread(getattr(self, ref).add, idx)
            reactor.callInThread(getattr(self, ref).set, idx)
            reactor.callInThread(getattr(self, ref).inc)

        # threads should be done with the work
        time.sleep(0.01)

    def assertDataNotEqual(self, result, ref):
        self.assertNotEqual(getattr(self, ref).data, EXPECTED)

    def assertSumsNotEqual(self, result, ref):
        self.assertNotEqual(
            sum(getattr(self, ref).container), sum(EXPECTED)
        )

    def test_ThreadNeverafeSingleton_is_unsafe(self):
        deferred = defer.Deferred()
        deferred.addCallback(self._do_junk, 'neversafe')
        deferred.addCallback(self.assertDataNotEqual, 'neversafe')
        deferred.addCallback(self.assertSumsNotEqual, 'neversafe')
        reactor.callLater(0, deferred.callback, None)
        return deferred

    def test_ThreadAddNotSafeSingleton_is_unsafe(self):
        deferred = defer.Deferred()
        deferred.addCallback(self._do_junk, 'addnotsafe')
        deferred.addCallback(self.assertDataNotEqual, 'addnotsafe')
        deferred.addCallback(self.assertSumsNotEqual, 'addnotsafe')
        reactor.callLater(0, deferred.callback, None)
        return deferred

    def test_ThreadSetNotSafeSingleton_is_unsafe(self):
        deferred = defer.Deferred()
        deferred.addCallback(self._do_junk, 'setnotsafe')
        deferred.addCallback(self.assertDataNotEqual, 'setnotsafe')
        deferred.addCallback(self.assertSumsNotEqual, 'setnotsafe')
        reactor.callLater(0, deferred.callback, None)
        return deferred

    def test_lock_is_functional(self):
        ts = ThreadedSingleton()
        ts.acquire()
        # the following function will never run because we have already
        # acquired the lock in another thread in the previous statement and
        # won't ever let release it.
        reactor.callInThread(ts.wont_ever_run)
        # N.B. if callInThread is not used then the main reactor thread in
        # twisted would acquire the lock and the test would fail.
        self.assertEqual(ts.counter, 0)
