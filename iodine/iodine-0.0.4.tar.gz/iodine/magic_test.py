import unittest
from .main import get_salt_magic
from IPython.core.magic import Bunch
import logging
from getpass import getpass

logging.basicConfig(filename='iodine.log', level=logging.DEBUG)
username = getuser()
master = 'localhost'
password = None


class SaltMagicsTest(unittest.TestCase):
    def setUp(self):
        global password
        from IPython.terminal.embed import InteractiveShellEmbed
        ipshell = InteractiveShellEmbed()
        password = password or getpass('Password: ')
        self.magics = get_salt_magic(
            ipshell,
            username=username,
            master=master,
            password=password,
            no_cache=True,
        )

    def test_salt_completer_minions(self):
        event = Bunch()
        event.text_until_cursor = "salt "
        print(self.magics._salt_completer(None, event))

    def test_salt_completer_functions(self):
        event = Bunch()
        event.text_until_cursor = "salt * "
        print(self.magics._salt_completer(None, event))

    def test_salt_completer_functions_partial(self):
        event = Bunch()
        event.text_until_cursor = "salt * sys"
        print(self.magics._salt_completer(None, event))

    def test_salt(self):
        self.magics.salt('* test.rand_sleep max=10')
        ret = self.magics.result
        self.assertGreater(len(ret['return']), 0)
    def test_salt_long(self):
        self.magics.salt('AU03-VMHOSTUBS1 test.sleep 300')
        ret = self.magics.result
        self.assertGreater(len(ret['return']), 0)
    def test_salt_cmd(self):
        self.magics.salt('* cmd.run "C:/salt/mingw/bin/grep.exe --help"')
        ret = self.magics.result
        self.assertGreater(len(ret['return']), 0)

    def test_salt_grain(self):
        self.magics.salt('-G xplan:instances:* test.ping')
        ret = self.magics.result
        self.assertGreater(len(ret['return']), 0)

    def test_salt_runner(self):
        self.magics.salt_runner('test.arg foo')
        ret = self.magics.result
        self.assertEqual(ret['return'][0]['kwargs']['arg'][0], 'foo')

    def test_cache_run(self):
        self.magics._cache_run()
        self.assertIn('list_functions', self.magics.cache)
        self.assertIsInstance(self.magics.cache['list_functions'], dict)

    def test_cache_minions(self):
        self.magics._cache_minions()
        self.assertIn('minions', self.magics.cache)
        self.assertIsInstance(self.magics.cache['minions'], list)
