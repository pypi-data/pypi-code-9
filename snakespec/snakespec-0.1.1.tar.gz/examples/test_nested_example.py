from unittest import TestCase
from snakespec.snakespec import describe


class TestNestedExample(TestCase):
    def setUp(self):
        self.foo = 'foo'

    def it_should_run_normally(self):
        self.assertEqual(self.foo, 'foo')

    @describe
    class GivenSomeCircumstance(TestCase):
        def setUp(self):
            super(TestNestedExample.GivenSomeCircumstance, self).setUp()
            self.bar = 'bar'

        def it_should_inherit_setup(self):
            self.assertEqual(self.foo, 'foo')

        def it_should_use_its_own_setup(self):
            self.assertEqual(self.bar, 'bar')

        @describe
        class WhenSomethingHappens(TestCase):
            def setUp(self):
                super(TestNestedExample.GivenSomeCircumstance.WhenSomethingHappens, self).setUp()
                self.foobar = self.foo + self.bar

            def it_should_inherit_setup_from_all_ancestors(self):
                self.assertEqual(self.foobar, 'foobar')
