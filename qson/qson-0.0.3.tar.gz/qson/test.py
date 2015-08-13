import sys
import thread

import server
import client

test_server = server.Server(("0.0.0.0", 0), server.Handler)
port = test_server.port()

thread.start_new_thread(test_server.serve_forever, tuple())

test_client = client.client(port=port)
print test_client("key1")
print test_client("key2", {
    "test": "values"
})
print test_client("key2")
