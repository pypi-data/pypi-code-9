# Copyright (c) 2015, RedJack, LLC.
# All rights reserved.
#
# Please see the COPYING file in this distribution for license details.
import pytest


@pytest.yield_fixture
def edgescape_server():
    from akadata.test import FakeEdgeScapeServer
    from threading import Thread

    server = FakeEdgeScapeServer()
    server_thread = Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    yield server

    server.shutdown()
