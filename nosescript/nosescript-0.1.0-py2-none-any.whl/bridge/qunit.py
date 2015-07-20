import re
import logging
import unittest

LOG = logging.getLogger('nose.' + __name__)
current_require_path = ''


def escape_literal(name):
    return re.sub('[^a-zA-Z0-9.]', '_', name)


class JsException(Exception):
    def __init__(self, error):
        message = '{}: {}'.format(error.name, error.message)
        super(JsException, self).__init__(message)
        self.traceback = None
        for line in error.stack.splitlines()[:-1]:
            match = re.match('([^(@]*)(\(.*\))?@(.*):(\d*)', line)
            name, args, fname, lineno = match.groups()
            if not fname or 'qunit-api.js' in fname:
                continue
            if not name:
                name = '<Anonymous>'
            lineno = int(lineno)
            self.traceback = JsTraceback(name, fname, lineno, self.traceback)


class JsTraceback(object):
    def __init__(self, name, fname, line, tb_next=None):
        self.tb_frame = JsTraceFrame(JsTraceCode(fname, name), line)
        self.tb_lineno = line
        self.tb_next = tb_next


class JsTraceCode(object):
    def __init__(self, co_filename, co_name):
        self.co_filename = co_filename
        self.co_name = co_name


class JsTraceFrame(object):
    def __init__(self, f_code, f_lineno):
        self.f_code = f_code
        self.f_lineno = f_lineno
        self.f_globals = {}
        self.f_locals = {}


class QUnitModule(object):
    def __init__(self, name, hooks):
        self.name = escape_literal(name)
        self.hooks = hooks
        LOG.info('Found test module [%s]', self.name)


class QUnitCase(unittest.TestCase):
    def __init__(self, module, name, test, qunit):
        super(QUnitCase, self).__init__()
        self.module = module
        self.name = escape_literal(name)
        self.test = test
        self.qunit = qunit
        LOG.info('Found test case [%s]', self.id())

    def id(self):
        return '{}.{}'.format(self.module.name, self.name)

    def __eq__(self, other):
        return (super(QUnitCase, self).__eq__(other)
                and self.id() == other.id())

    def shortDescription(self):
        return self.id()

    def setUp(self):
        if self.module.hooks and 'beforeEach' in self.module.hooks:
            self.module.hooks['beforeEach']()

    def tearDown(self):
        if self.module.hooks and 'afterEach' in self.module.hooks:
            self.module.hooks['afterEach']()

    def run(self, result=None):
        self.result = result
        super(QUnitCase, self).run(result)

    def runTest(self):
        error = self.test()
        if error:
            e = JsException(error)
            self.result.addError(self, (JsException, e, e.traceback))


class QUnit(object):
    def __init__(self, ctx):
        super(QUnit, self).__init__()
        self.tests = set()
        self._current_module = None
        self.ctx = ctx
        ctx.add_global('QUnit', self)
        ctx.require('qunit-api.js')
        ctx.require('json2.js')

    def _module(self, name, hooks={}):
        self._current_module = QUnitModule(name, hooks)

    def _test(self, name, test):
        case = QUnitCase(self._current_module, name, test, self)
        self.tests.add(case)

    def warn(self, msg):
        LOG.warn(msg)
