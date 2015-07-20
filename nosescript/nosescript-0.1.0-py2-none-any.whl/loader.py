import os
import logging
import spidermonkey
import pkg_resources

from .bridge.qunit import QUnit

LOG = logging.getLogger('nose.' + __name__)
RES_PATH = 'nosescript.resources'
LOG.info('initializing js runtime')
_runtime = spidermonkey.Runtime()


class JsContext(object):
    def __init__(self, path=[]):
        super(JsContext, self).__init__()
        self._ctx = _runtime.new_context()
        self._ctx.add_global('require', self.require)
        self.path = []
        self._path_stack = []
        self._js_modules = set()

    def execute(self, *args, **kwargs):
        if 'filename' in kwargs:
            self._path_stack.append(os.path.dirname(kwargs['filename']))
        return self._ctx.execute(*args, **kwargs)

    def add_global(self, *args, **kwargs):
        return self._ctx.add_global(*args, **kwargs)

    def load_script(self, path):
        if path in self._js_modules:
            return

        if os.path.isfile(path):
            self._path_stack.append(os.path.dirname(path))
            self._js_modules.add(path)
            with open(path) as f:
                script = f.read()
                return self._ctx.execute(script, filename=path)

    def require(self, name):
        path = name
        LOG.info('require(%s)', name)
        if not path.endswith('.js'):
            path += '.js'

        # absolute path
        if path.startswith('/'):
            return self.load_script(path)
            # TODO scan other config paths
        elif path.startswith('./'):
            # FIXME relative to current file in imports
            if not self._path_stack:
                raise RuntimeError("relative require cannot be at top-level")
            return self.load_script(os.path.join(self._path_stack[-1], path))
        else:
            r_string = pkg_resources.resource_string(RES_PATH, path)
            r_path = pkg_resources.resource_filename(RES_PATH, path)
            self._ctx.execute(r_string, filename=r_path)
            return

        raise RuntimeError("require not found " + path)


class TestRunner(object):
    def __init__(self, path, conf):
        super(TestRunner, self).__init__()
        self._ctx = JsContext()
        self._path = path
        self._qunit = QUnit(self._ctx)

    def load_tests(self):
        path = self._path
        LOG.info('Loading tests from %s', path)

        # set default module name as file name
        mod_name = os.path.basename(path).rpartition(os.path.extsep)[0]
        self._qunit.module(mod_name)

        self._ctx.require(path)
        for test in self._qunit.tests:
            yield test
        if not len(self._qunit.tests):
            yield False
