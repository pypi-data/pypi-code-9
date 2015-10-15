import unittest
from transat.server.client import Client
from transat.server.server import Server
import threading
import shutil
import os

class TestClient(unittest.TestCase):
    def setUp(self):
        se = Server()
        server = threading.Thread(target=se.run)
        server.daemon = True
        server.start()
        url = se.get_address()

        self.server = server
        self.client = Client(address=url)

        self.dir = "tmp"
        if os.path.exists(self.dir):
            shutil.rmtree(self.dir)
        os.mkdir(self.dir)

    def test_userinterrupt_stop_simulation(self):
        pass
        #self.client.run(self.dir, nprocs=1)
        #self.client.watch(None)


