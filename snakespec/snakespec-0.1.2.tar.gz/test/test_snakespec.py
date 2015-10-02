import os
from unittest import TestCase
from nose.plugins import PluginTester
from snakespec.snakespec import SnakeSpec


class SnakeSpecTester(PluginTester, TestCase):
    activate = '--snakespec'
    plugins = [SnakeSpec()]


class TestNestedExample(SnakeSpecTester):
    suitepath = os.path.join(os.getcwd(), 'examples', 'test_nested_example.py')

    def test_it_should_run_all_tests(self):
        assert 'Ran 4 tests' in self.output
        assert 'FAILED' not in self.output
        assert 'ERROR' not in self.output


class TestMultipleChildrenExample(SnakeSpecTester):
    suitepath = os.path.join(os.getcwd(), 'examples', 'test_multiple_children_example.py')

    def test_it_should_run_all_tests(self):
        assert 'Ran 9 tests' in self.output
        assert 'FAILED' not in self.output
        assert 'ERROR' not in self.output


class TestHamcrestExample(SnakeSpecTester):
    suitepath = os.path.join(os.getcwd(), 'examples', 'test_hamcrest_example.py')

    def test_test_it_should_work_with_hamcrest(self):
        assert 'Ran 3 tests' in self.output
        assert 'FAILED' not in self.output
        assert 'ERROR' not in self.output
