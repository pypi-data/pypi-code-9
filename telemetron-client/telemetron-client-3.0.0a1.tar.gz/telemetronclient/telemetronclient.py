"""
Telemetron client module.
"""

import socket
import time
import logging
import random
import uuid

import certifi
import urllib3

from . import __version__


def api_client_user_agent():
    """
    Returns the string of User-Agent to use in api calls.
    """
    return 'Telemetron-client-python/%s' % (__version__,)


class TelemetronClientException(Exception):
    """
    Base class for every Telemetron Client exception
    """
    pass


class BufferSizeTooLarge(TelemetronClientException):
    """
    BufferSizeTooLarge class
    """
    pass


class TelemetronClient(object):
    """
    This class represents the telemetron Client.
    It handles the socket connection to a telemetron server and has the
    ability to construct metric lines.
    """
    defaultNS = "application"

    TRANSPORT_TCP = "tcp"
    TRANSPORT_UDP = "udp"
    TRANSPORT_API = "api"
    TRANSPORT_API_SSL = "api+ssl"

    def __init__(self, host="127.0.0.1", port=2013, prefix="client",
                 transport="udp", sample_rate=None, app="application",
                 api_timeout=2.0, api_path="/tel/v2.0/metrics",
                 api_token=None, init_transport=True, max_buffer_size=1000):
        """
        Constructor.

        Keyword arguments:
        host -- is telemetron's server host or ip
        port -- is telemetron's server port
        prefix -- is the prefix string to use in metrics
        transport -- is either udp or tcp
        sample_rate -- is the sampling rate in percent 1 to 99
        init_transport -- if True, will call init_transport() immediately
        max_buffer_size -- the max buffer size allowed
        """

        self.log = logging.getLogger("telemetronclient")

        self.host = host
        self.port = port
        self.transport = transport
        self.prefix = prefix

        self.api_timeout = api_timeout
        self.api_path = api_path
        self.api_token = api_token

        if sample_rate is not None and (sample_rate < 1 or sample_rate > 99):
            raise ValueError("Sample rate out of range")

        self.sample_rate = sample_rate
        self.app = app

        self._buffer = []
        self._socket = None
        self.max_buffer_size = max_buffer_size

        valid_apis = (
            self.TRANSPORT_TCP,
            self.TRANSPORT_UDP,
            self.TRANSPORT_API,
            self.TRANSPORT_API_SSL
            )

        if transport.lower() not in valid_apis:
            raise ValueError()

        if init_transport:
            self.init_transport()


    def init_transport(self):
        """
        Do whatever is necessary to initialize the transport.

        In case of:
        TCP - connect to endpoint
        UDP - just open the socket
        API - initialize an http(s) connection pool
        """
        self.log.info("Initializing transport %s", self.transport)
        if self.transport.lower() == self.TRANSPORT_TCP:
            if self._socket is None:
                self._socket = socket.socket(socket.AF_INET,
                                             socket.SOCK_STREAM)
            self._socket.connect((self.host, self.port))
        elif self.transport.lower() == self.TRANSPORT_UDP:
            if self._socket is None:
                self._socket = socket.socket(socket.AF_INET,
                                             socket.SOCK_DGRAM)
        elif self.transport.lower() == self.TRANSPORT_API:
            self._pool = urllib3.HTTPConnectionPool(
                self.host,
                port=self.port,
                maxsize=1
                )
        elif self.transport.lower() == self.TRANSPORT_API_SSL:
            self._pool = urllib3.HTTPSConnectionPool(
                self.host,
                port=self.port,
                maxsize=1,
                cert_reqs='CERT_REQUIRED', # Force certificate check.
                ca_certs=certifi.where(),  # Path to the Certifi bundle.
                )

    def end_transport(self):
        """
        Clean up needed resources allocated by the current transport method.
        """
        self.log.debug("Cleaning up transport %s", self.transport)

        if self._socket is not None:
            self._socket.close()

    def time(self, name, value, tags=None, agg=None,
             agg_freq=10, namespace=defaultNS, timestamp=None):
        """
        Sends a timing metric

        Keyword arguments:
        name -- Name of the counter. Ex: response_time
        value -- the value
        tags -- Tags to associate this value with, for example {from:
        'serviceA', to: 'serviceB', method: 'login'}
        agg -- List of aggregations to be applied by the Telemetron.
        Ex: ['avg', 'p90', 'min']
        agg_freq -- Aggregation frequency in seconds. One of: 10, 15, 30,
        60 or 300
        namespace -- Define the metric namespace. Default: application
        timestamp -- is the timestamp associated with the metric. If not
        set, will use current time (utc)
        """
        if tags is None:
            tags = {}
        if agg is None:
            agg = ['avg', 'p90', 'count', 'count_ps']

        tags.update({"unit": 'ms'})
        self.put(
            'timer.%s' % (name,),
            tags,
            value | 0,
            agg,
            agg_freq,
            self.sample_rate,
            namespace,
            timestamp)

    def inc(self, name, value, tags=None, agg=None,
            agg_freq=10, namespace=defaultNS, timestamp=None,):
        """
        Increments a counter

        Keyword arguments:
        name -- Name of the counter. Ex: transactions
        value
        tags -- Tags to associate this value with, for example {type:
        'purchase_order'}
        agg -- List of aggregations to be applied by the Telemetron. Ex:
        ['avg', 'p90', 'min']
        agg_freq -- Aggregation frequency in seconds. One of: 10, 15, 30,
        60 or 300
        namespace -- Define the metric namespace. Default: application
        timestamp -- is the timestamp associated with the metric. If not
        set, will use current time (utc)
        """

        if tags is None:
            tags = {}
        if agg is None:
            agg = ['sum', 'count', 'count_ps']

        self.put('counter.%s' % (name,),
                 tags,
                 value | 0,
                 agg,
                 agg_freq,
                 self.sample_rate,
                 namespace,
                 timestamp)

    def gauge(self, name, value, tags=None, agg=None, agg_freq=10,
              namespace=defaultNS, timestamp=None):
        """
        Adds a Gauge

        Keyword arguments:
        name -- Name of the Gauge. Ex: current_sessions
        value
        tags -- Tags to associate this value with, for example {page:
        'overview'}
        agg -- List of aggregations to be applied by the Telemetron.
        Ex: ['avg', 'p90', 'min']
        agg_freq -- Aggregation frequency in seconds. One of: 10, 15, 30,
        60 or 300
        namespace -- Define the metric namespace. Default: application
        timestamp -- is the timestamp associated with the metric. If not
        set, will use current time (utc)
        """
        if tags is None:
            tags = {}
        if agg is None:
            agg = ['last']

        self.put('gauge.%s' % (name,),
                 tags,
                 value | 0,
                 agg,
                 agg_freq,
                 self.sample_rate,
                 namespace,
                 timestamp)

    def put(self, metric, tags, value, agg=None, agg_freq=10,
            sample_rate=None, namespace=defaultNS, timestamp=None):
        """
        Adds a new metric to the in-memory buffer.

        Keyword arguments:
        metric -- Name metric such as "response_time"
        tags -- Tags to associate this value with, for example
        {from: 'serviceA', to: 'serviceB', method: 'login'}
        value
        agg -- List of aggregations to be applied by the Telemetron.
        Ex: ['avg', 'p90', 'min']
        agg_freq -- Aggregation frequency in seconds. One of: 10, 15, 30,
        60 or 300
        sample_rate -- Sampling rate (1-99)
        timestamp -- is the timestamp associated with the metric. If not
        set, will use current time (utc)
        """
        if agg is None:
            agg = []

        if sample_rate is not None and (sample_rate < 1 or sample_rate > 99):
            raise ValueError("Sample rate out of range")

        sample_rate_normalized = (sample_rate or 100.0) / 100.0

        if random.random() <= sample_rate_normalized:

            if self.app:
                tags["app"] = self.app

            line = self.make_line(metric, tags, value, agg, agg_freq,
                                  sample_rate, namespace, timestamp)
            self.put_raw(line)

    def put_raw(self, lines):
        """
        Insert a raw line into the buffer (use with caution)

        Keyword arguments:
        lines -- if lines is a list, insert every element into the buffer.
        If it's a single line, insert it into the buffer.

        Raises BufferSizeTooLarge if buffer size is at max_buffer_size
        """
        if len(self._buffer) >= self.max_buffer_size:
            raise BufferSizeTooLarge

        self.log.debug("Appending line(s) to buffer %s", lines)

        if isinstance(lines, list):
            for l in lines:
                self._buffer.append(l)
        else:
            self._buffer.append(lines)

    def make_line(self, metric, tags, value, agg=None, agg_freq=10,
                  sample_rate=None, namespace=defaultNS, timestamp=None):
        """
        Generate a metric line

        Keyword arguments:
        metric -- Name metric such as "response_time"
        tags -- Tags to associate this value with, for example
        {from: 'serviceA', to: 'serviceB', method: 'login'}
        value
        agg -- List of aggregations to be applied by the Telemetron.
        Ex: ['avg', 'p90', 'min']
        agg_freq -- Aggregation frequency in seconds. One of: 10, 15, 30,
        60 or 300
        sample_rate -- Sampling rate (1-99)
        timestamp -- is the timestamp associated with the metric. If not
        set, will use current time (utc)

        Returns metric line string
        """
        if agg is None:
            agg = []

        def concat(prev, tag):
            """ concat function to be used with reduce() """
            return "%s,%s=%s" % (prev, tag, tags[tag])

        metricName = "%s.%s.%s" % (self.prefix, namespace, metric)
        line = reduce(concat, tags, metricName)
        line += " %s %d" % (value, timestamp or int(time.time()))
        if len(agg) > 0 and agg_freq:
            aggCopy = list(agg)
            aggCopy.append(agg_freq)
            line += " %s" % (','.join([str(a) for a in aggCopy]),)
            if sample_rate:
                line += " %s" % (sample_rate,)
        return line

    def flush(self, send_buffer_length=True):
        """
        Flush buffer to socket

        Keyword arguments:
        send_buffer_length -- if True, appends a metric to the buffer with
            the current buffer length
        """
        if len(self._buffer) > 0:
            if send_buffer_length:
                self.put('buffer.flush_length',
                         {},
                         len(self._buffer),
                         ['avg'])
            message = "%s\n" % ("\n".join(self._buffer),)
            self.log.info(
                "About to flush %d lines on a %d byte message",
                len(self._buffer),
                len(message))
            self.log.debug("Whole message to be flushed: %s", message)

            if self.transport.lower() == self.TRANSPORT_TCP:
                self._socket.sendall(message)
            elif self.transport.lower() == self.TRANSPORT_UDP:
                sent = self._socket.sendto(message, (self.host, self.port))
                self.log.info("%s transport bytes sent %d",
                              self.transport, sent)
            elif self.transport.lower() == self.TRANSPORT_API\
            or self.transport.lower() == self.TRANSPORT_API_SSL:
                boundary = uuid.uuid4()

                headers = {
                    "User-Agent": api_client_user_agent(),
                    "M-Api-Token": self.api_token,
                    "content-type": "multipart/related; boundary=%s" % (
                        boundary,)
                }

                body = "--%(boundary)s\n\n%(message)s--%(boundary)s--" % {
                    'boundary': boundary,
                    'message': message
                }
                res = self._pool.request(
                    'PUT',
                    self.api_path,
                    headers=headers,
                    timeout=self.api_timeout,
                    body=body
                    )

                self.log.info("%s transport return code is %s",
                              self.transport, res.status)

                if res.status != 201:
                    return False

            self._buffer = []
            return True

    def buffer_count(self):
        """
        Returns the current number of messages in buffer.
        """
        return len(self._buffer)


class AutoFlushTelemetronClient(TelemetronClient):
    """
    AutoFlushClient

    A version of Client that auto flushes when a specific buffer size is hit.
    """

    def __init__(self, flush_size=30, *args, **kws):
        """
        Constructor

        Keyword arguments:
        flush_size -- is the buffer size at which a flush should be
        triggered.
        """

        self.flush_size = flush_size
        self._do_flush = True

        super(AutoFlushTelemetronClient, self).__init__(*args, **kws)

    def put_raw(self, lines):
        super(AutoFlushTelemetronClient, self).put_raw(lines)

        #  Prevents an infinite method call loop
        if self._do_flush and self.buffer_count() >= self.flush_size:
            self._do_flush = False
            self.flush()
            self._do_flush = True
