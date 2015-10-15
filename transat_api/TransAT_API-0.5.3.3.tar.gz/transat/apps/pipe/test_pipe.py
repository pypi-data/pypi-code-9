import sys
import unittest

sys.path.append("apps/pipe")
from transat.apps.pipe.pipe import my_fun
import transat.appbuilder as appbuilder
from transat.server.server import Server
import threading


class TestPipeApp(unittest.TestCase):
    def test_runApp(self):
        app = appbuilder.App('Pipe')
        app.add_main(my_fun)
        se = Server()
        server = threading.Thread(target=se.run)
        server.daemon = True
        server.start()
        dp = app.run({'address': se.get_address()})
        self.assertAlmostEqual(dp, 0.70924037191)

    test_runApp.heavy = True


