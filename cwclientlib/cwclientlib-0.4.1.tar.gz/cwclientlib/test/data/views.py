#

from cubicweb.web.views.basecontrollers import ViewController


class TestController(ViewController):
    __regid__ = 'test-controller'

    def publish(self, rset=None):
        return "coucou"
