from inspect import getmembers
from os import environ
from os.path import sep
import re
from types import MethodType
from nose.plugins import Plugin


def describe(test_case):
    test_case._is_describe = True
    return test_case


class SnakeSpec(Plugin):
    env_option = 'NOSE_SNAKESPEC'

    def __init__(self):
        super(SnakeSpec, self).__init__()

    def options(self, parser, env=None):
        env = env or environ
        super(SnakeSpec, self).options(parser, env=env)

        enabled = bool(env.get(self.env_option, False))

        parser.add_option(
            '--snakespec',
            action='store_true',
            default=enabled,
            dest='snakespec',
            help='enable bdd-style testing with snakespec (or set ${}=true'.format(
                self.env_option,
            ),
        )
        parser.add_option(
            '--no-snakespec',
            action='store_false',
            dest='snakespec',
            help='disable bdd-style testing with snakespec',
        )

    def configure(self, options, conf):
        super(SnakeSpec, self).configure(options, conf)
        if options.snakespec:
            bdd_pattern = r'(?:^|[\b_\.{sep}-])(?:[Tt]est|[Ii]t|[Ss]hould|[Tt]hen)'.format(sep=sep)
            self.enabled = True
            self.conf.testMatch = re.compile(bdd_pattern)

    def loadTestsFromTestCase(self, cls):
        # hisssssssssssssssssssss
        # oh so grossssssssssssss
        for (name, member) in getmembers(cls, self._is_describe):

            member_name = member.__name__
            descendant = type(member_name, (cls,), member.__dict__.copy())
            delattr(descendant, '_is_describe')
            setattr(cls, member_name, descendant)

            for (key, val) in getmembers(member, self._is_test):
                yield self._get_test_from_case(descendant, val)
            for test_case in self.loadTestsFromTestCase(descendant):
                yield test_case

    def _is_describe(self, obj):
        return getattr(obj, '_is_describe', False)

    def _is_test(self, obj):
        return isinstance(obj, MethodType) and self.conf.testMatch.search(obj.im_func.func_name)

    def _get_test_from_case(self, test_case, test):
        return test_case(test.im_func.func_name)
