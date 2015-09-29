"""
Telemetron client package.
"""

import socket
import time
import logging
import random

__version__ = "2.3"


class TelemetronClient(object):
    """
    This class represents the telemetron Client.
    It handles the socket connection to a telemetron server and has the
    ability to construct metric lines.
    """
    defaultNS = "application"

    TCP_SOCKET = "tcp"
    UDP_SOCKET = "udp"


    def __init__(self, host="127.0.0.1", port=2013, prefix="client",
                 socket_type="udp", sample_rate=None, start_socket=True):
        """
        Constructor.

        Keyword arguments:
        host -- is telemetron's server host or ip
        port -- is telemetron's server port
        prefix -- is the prefix string to use in metrics
        socket_type -- is either udp or tcp
        sample_rate -- is the sampling rate in percent 1 to 99
        start_socket -- if True, will call startSocket() immediately
        """
        self.host = host
        self.port = port
        self.socketType = socket_type
        self.prefix = prefix

        if sample_rate is not None and (sample_rate < 1 or sample_rate > 99):
            raise ValueError("Sample rate out of range")

        self.sampleRate = sample_rate

        self._lastFlush = 0
        self._buffer = []
        self._socket = None

        if socket_type.lower() not in ("udp", "tcp"):
            raise ValueError()

        if start_socket:
            self.startSocket()


    def startSocket(self):
        """
        Start the socket.
        If socket was already initialized, just connect to endpoint (in TCP mode).
        """
        if self.socketType.lower() == 'tcp':
            if self._socket is None:
                self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((self.host, self.port))
        elif self.socketType.lower() == 'udp':
            if self._socket is None:
                self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def closeSocket(self):
        """
        Close the socket
        """
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
            self.sampleRate,
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
                 self.sampleRate,
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
                 self.sampleRate,
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
            line = self.makeLine(metric, tags, value, agg, agg_freq,
                                 sample_rate, namespace, timestamp)
            self.putRaw(line)

    def putRaw(self, lines):
        """
        Insert a raw line into the buffer (use with caution)

        Keyword arguments:
        lines -- if lines is a list, insert every element into the buffer.
        If it's a single line, insert it into the buffer.
        """
        if isinstance(lines, list):
            for l in lines:
                self._buffer.append(l)
        else:
            self._buffer.append(lines)

    def makeLine(self, metric, tags, value, agg=None, agg_freq=10,
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
            if self.socketType.lower() == 'tcp':
                self._socket.sendall(message)
            elif self.socketType.lower() == 'udp':
                self._socket.sendto(message, (self.host, self.port))
            self._buffer = []
            self._lastFlush = time.time()

    def bufferCount(self):
        """
        Returns the current number of messages in buffer.
        """
        return len(self._buffer)

    def timeSinceFlush(self):
        """
        Returns elapsed time, in seconds, since last successful flush call
        """
        if self._lastFlush:
            return time.time() - self._lastFlush
        return 0



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

        self.flushSize = flush_size
        self._doFlush = True

        super(AutoFlushTelemetronClient, self).__init__(*args, **kws)


    def putRaw(self, lines):
        super(AutoFlushTelemetronClient, self).putRaw(lines)

        #  Prevents an infinite method call loop
        if self._doFlush and self.bufferCount() >= self.flushSize:
            self._doFlush = False
            self.flush()
            self._doFlush = True
