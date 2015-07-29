__test__ = False


def setup():
    pass


from nose.suite import ContextSuite

ContextSuite.moduleSetup = ('setup_module', 'setupModule', 'setUpModule', 'setupHolder', 'setUp')
