import json
import time
import socket

from zope.interface import implements

from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.internet.defer import succeed
from twisted.web.iweb import IBodyProducer


class JSONProducer(object):
    implements(IBodyProducer)

    def __init__(self, body):
        self.body = json.dumps(body)
        self.length = len(self.body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass


def metric(metric, value, host=None, tags=None, type='gauge', timestamp=None):
    if timestamp is None:
        timestamp = time.time()
    if host is None:
        host = socket.gethostname()
    return {
        'metric': metric,
        'points': [(timestamp, value)],
        'type': type,
        'host': host,
        'tags': tags,
    }


class DataDog(object):

    endpoint = 'https://app.datadoghq.com/api'
    version = 1

    def __init__(self, reactor, api_key):
        self.api_key = api_key
        self.client = Agent(reactor)

    def _get_url(self, action):
        return '{}/v{}/{}?api_key={}'.format(
            self.endpoint,
            self.version,
            action,
            self.api_key,
        )

    def _request(self, method, action, **kwargs):
        url = self._get_url(action)
        return self.client.request(method, url, **kwargs)

    def _post(self, action, body):
        return self._request(
            'POST', action,
            headers=Headers({'Content-Type': ['application/json']}),
            bodyProducer=JSONProducer(body),
        )

    def metric(self, *args, **kwargs):
        return self.multi_metric([metric(*args, **kwargs)])

    def multi_metric(self, metrics):
        d = self._post('series', {'series': metrics})
        d.addCallback(self.handle_response)
        return d

    def handle_response(self, r):
        assert r.code in (200, 201, 202, 204)
