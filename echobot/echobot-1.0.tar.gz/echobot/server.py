from functools import partial
import asyncio

class EchoBotServer(object):
    def __init__(self):
        self.client_map = {}

        for client_key, client in enumerate(self.clients):
            self.client_map[client_key] = client(partial(self.broadcast_msg, client_key))

        i = asyncio.get_event_loop()

        i.run_forever()
        i.close()

    def broadcast_msg(self, client_key, msg):
        for send_client_key, client in self.client_map.items():
            if client_key == send_client_key:
                continue
            asyncio.async(client.send_msg(msg))
