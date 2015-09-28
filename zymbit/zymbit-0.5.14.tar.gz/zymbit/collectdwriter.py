import collections
import json
import socket
import threading

AGGREGATES_LOCK = threading.Lock()


class MetricsAggregator(object):
    """
    Collects and groups
    """
    max_age = 1.0  # seconds
    value_names = {
        'disk': ('written', 'read'),
        'interface': ('tx', 'rx'),
        'load': ('1min', '5min', '15min'),
    }

    def __init__(self):
        # dict of string:metric_name, dict:data pairs
        # the data dict will contain a `time` key indicating the time the first entry came in
        self.aggregates = collections.OrderedDict()

    def aggregate(self, metric):
        ready = []

        # upstream expects time in milliseconds
        _time = metric.time * 1000

        with AGGREGATES_LOCK:
            # collect metrics that are ready to be shipped
            keys = self.aggregates.keys()
            for key in keys:
                if self.is_ready(self.aggregates[key], _time):
                    ready.append(self.aggregates.pop(key))
                else:
                    break  # this is a sorted dict, so if the top isn't ready, later items won't be either

            basename = name = metric.type

            instance = metric.plugin_instance
            if instance:
                name = '{}.{}'.format(basename, instance)

            aggregate = self.aggregates.setdefault(name, {
                'key': name,
                'time': _time
            })

        # make sure the time in the aggregate is the first timestamp in this series
        aggregate['time'] = min(aggregate['time'], _time)

        metric_name = metric.type_instance or metric.plugin
        aggregate.update(self.get_values(metric_name, metric.values))

        return ready

    def get_values(self, metric_name, values):
        value_names = self.value_names.get(metric_name, [metric_name])
        return dict(zip(value_names, values))

    def is_ready(self, aggregate, time):
        return aggregate['time'] + self.max_age < time


class MetricsMessenger(object):
    """
    Ships metrics to the local messenger service
    """
    config = {}

    def __init__(self, aggregator=None):
        self._addr = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.aggregator = aggregator or MetricsAggregator()

    @property
    def addr(self):
        if self._addr:
            return self._addr

        self._addr = (
            self.config.get('host', 'localhost'),
            self.config.get('port', 9628),
        )

        return self._addr

    def write(self, buf):
        for metric in self.aggregator.aggregate(buf):
            prefix = self.config.get('prefix')
            if prefix:
                metric['key'] = '{}.{}'.format(prefix, metric['key'])

            self.sock.sendto(json.dumps(metric), self.addr)


MESSENGER = MetricsMessenger()


def config(config_item):
    """
    child: host, values: ('localhost',)
    child: port, values: ('8001',)
    """
    MESSENGER.config.update([(x.key, x.values[0]) for x in config_item.children])


def write(metric, data=None):
    MESSENGER.write(metric)
