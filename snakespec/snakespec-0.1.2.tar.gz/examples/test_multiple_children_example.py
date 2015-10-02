from unittest import TestCase
import nose
from snakespec.snakespec import describe, SnakeSpec


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

            def it_should_support_multiple_children(self):
                self.assertNotEqual(1 + 1, 3)

    @describe
    class GivenAnotherCircumstance(TestCase):
        def setUp(self):
            super(TestNestedExample.GivenAnotherCircumstance, self).setUp()
            self.bar = 'barbar'

        def it_should_inherit_setup(self):
            self.assertEqual(self.foo, 'foo')

        def it_should_use_its_own_setup(self):
            self.assertEqual(self.bar, 'barbar')

        @describe
        class WhenSomethingElseHappens(TestCase):
            def setUp(self):
                super(TestNestedExample.GivenAnotherCircumstance.WhenSomethingElseHappens, self).setUp()
                self.foobar = self.foo + self.bar

            def it_should_inherit_setup_from_all_ancestors(self):
                self.assertEqual(self.foobar, 'foobarbar')

            def it_should_support_multiple_children(self):
                self.assertEqual(1 + 1, 2)


if __name__ == '__main__':
    nose.main(addplugins=[SnakeSpec()])
