import json
import urllib2

import server

HOST = "localhost"

class client(object):
    def __init__(self, host=HOST, port=server.PORT, protocol="http"):
        super(client, self).__init__()
        self.host = host
        self.port = port
        self.protocol = protocol

    def post(self, data):
        url = "{0}://{1}:{2}/".format(self.protocol, self.host, self.port)
        req = urllib2.Request(url, data, {"Content-Type": "application/json"})
        response = urllib2.urlopen(req)
        return response

    def send(self, data):
        key = data["key"]
        data = json.dumps(data)
        response = self.post(data)
        try:
            response = json.load(response)
        except Exception:
            response = {
                "key": key,
                "value": None,
            }
        return response

    def set(self, key, value):
        data = {
            "key": key,
            "value": value,
        }
        return self.send(data)["value"]

    def get(self, key):
        data = {
            "key": key,
        }
        return self.send(data)["value"]

    def __call__(self, key, value=False):
        if value:
            return self.set(key, value)
        return self.get(key)
