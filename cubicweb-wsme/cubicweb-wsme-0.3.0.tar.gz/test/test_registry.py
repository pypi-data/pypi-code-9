from contextlib import contextmanager

from cubicweb.devtools import testlib

pause_trace = testlib.pause_trace


@contextmanager
def dummy_pause_trace():
    yield


class DisablePauseTraceContext(object):
    def __enter__(self):
        pass

    def __exit__(self, *args):
        testlib.pause_trace = pause_trace


def disable_pause_trace():
    testlib.pause_trace = dummy_pause_trace
    return DisablePauseTraceContext()


def enable_pause_trace():
    testlib.pause_trace = pause_trace


class RegistryTests(testlib.CubicWebTC):
    def setUp(self):
        disable_pause_trace()
        super(RegistryTests, self).setUp()

    def tearDown(self):
        super(RegistryTests, self).tearDown()
        enable_pause_trace()

    def test_wsme_registry(self):
        r = self.vreg.wsme_registry
        self.assertIs(self.vreg.wsme_registry, r)
