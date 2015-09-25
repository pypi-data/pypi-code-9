from unittest import TestCase
from .singletons import Singleton, SingletonPrime

import mock


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
        self.catalog.registry['foo'] = 'bar'
        self.catalog.reset()
        self.assertEqual(self.catalog.registry, {})

    def test_mixins_work_with_attr_assignment(self):
        self.frank.name = 'sam'
        self.assertEqual(self.frank.hello(), 'sup sam')

    def test_mixins_work(self):
        self.assertEqual(self.frank.hello(), 'nope')


class StillSingletonPrime(SingletonPrime):

    def setUp(self):
        self.foo = 'bar'


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
        self.assertRaises(AttributeError, getattr, b, 'foo')

    def test_inheritance_works_when_instantiation_is_clean(self):
        b = StillSingletonPrime()
        self.assertEqual(b.foo, 'bar')
