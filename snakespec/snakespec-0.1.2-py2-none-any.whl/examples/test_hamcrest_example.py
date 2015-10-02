from unittest import TestCase
from hamcrest import *
from snakespec.snakespec import describe


class TestHamcrestExample(TestCase):
    def setUp(self):
        self.array = ['foo']

    def it_should_work_with_hamcrest(self):
        assert_that(self.array, contains('foo'))
        assert_that(self.array, not_(contains('bar')))

    @describe
    class WhenSetupIsNested(TestCase):
        def setUp(self):
            super(TestHamcrestExample.WhenSetupIsNested, self).setUp()
            self.array.append('bar')

        def it_should_inherit_setup(self):
            assert_that('foo', is_in(self.array))

        def it_should_use_its_own_setup(self):
            assert_that(self.array, contains_inanyorder('foo', 'bar'))
