import os
from unittest import TestCase
from nose.plugins import PluginTester
from snakespec.snakespec import SnakeSpec


class TestNestedExample(PluginTester, TestCase):
    activate = '--snakespec'
    plugins = [SnakeSpec()]
    suitepath = os.path.join(os.getcwd(), 'examples', 'test_nested_example.py')

    def it_should_run_all_tests(self):
        assert 'Ran 4 tests' in self.output
        assert 'FAILED' not in self.output
        assert 'ERROR' not in self.output

