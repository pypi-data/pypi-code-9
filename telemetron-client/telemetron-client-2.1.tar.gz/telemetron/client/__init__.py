"""
telemetron.Client module
"""

import socket
import time
import logging
import random

__version__ = "2.1"


class Client(object):
    """
    This class represents the telemetron Client.
    It handles the socket connection to a telemetron server and has the
    ability to construct metric lines.
    """
    defaultNS = "application"

    TCP_SOCKET = "tcp"
    UDP_SOCKET = "udp"


    def __init__(self, host="127.0.0.1", port=2013, prefix="client",
                 socket_type="udp", sample_rate=100.0, start_socket=True):
        """
        Constructor.

        @param host is telemetron's server host or ip
        @param port is telemetron's server port
        @param prefix is the prefix string to use in metrics
        @param socket_type is either udp or tcp
        @param sample_rate is the sampling rate in percent 1 to 99
        @param start_socket if True, will call startSocket() immediately
        """
        self.host = host
        self.port = port
        self.socketType = socket_type
        self.prefix = prefix
        self._buffer = []
        self._socket = None
        self.sampleRate = sample_rate
        self._lastFlush = 0

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

        @param name Name of the counter. Ex: response_time
        @param value
        @param tags Tags to associate this value with, for example {from:
        'serviceA', to: 'serviceB', method: 'login'}
        @param agg List of aggregations to be applied by the Telemetron.
        Ex: ['avg', 'p90', 'min']
        @param agg_freq Aggregation frequency in seconds. One of: 10, 15, 30,
        60 or 300
        @param namespace Define the metric namespace. Default: application
        @param timestamp is the timestamp associated with the metric. If not
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

        @param name Name of the counter. Ex: transactions
        @param value
        @param tags Tags to associate this value with, for example {type:
        'purchase_order'}
        @param agg List of aggregations to be applied by the Telemetron. Ex:
        ['avg', 'p90', 'min']
        @param agg_freq Aggregation frequency in seconds. One of: 10, 15, 30,
        60 or 300
        @param namespace Define the metric namespace. Default: application
        @param timestamp is the timestamp associated with the metric. If not
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

        @param name Name of the Gauge. Ex: current_sessions
        @param value
        @param tags Tags to associate this value with, for example {page:
        'overview'}
        @param agg List of aggregations to be applied by the Telemetron.
        Ex: ['avg', 'p90', 'min']
        @param agg_freq Aggregation frequency in seconds. One of: 10, 15, 30,
        60 or 300
        @param namespace Define the metric namespace. Default: application
        @param timestamp is the timestamp associated with the metric. If not
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
            sample_rate=100.0, namespace=defaultNS, timestamp=None):
        """
        Adds a new metric to the in-memory buffer.

        @param metric Name metric such as "response_time"
        @param tags Tags to associate this value with, for example
        {from: 'serviceA', to: 'serviceB', method: 'login'}
        @param value
        @param agg List of aggregations to be applied by the Telemetron.
        Ex: ['avg', 'p90', 'min']
        @param agg_freq Aggregation frequency in seconds. One of: 10, 15, 30,
        60 or 300
        @param sample_rate Sampling rate (1-99)
        @param timestamp is the timestamp associated with the metric. If not
        set, will use current time (utc)
        """
        if agg is None:
            agg = []

        sample_rate_normalized = sample_rate / 100.0
        if random.random() <= sample_rate_normalized:
            line = self.makeLine(metric, tags, value, agg, agg_freq,
                                 sample_rate, namespace, timestamp)
            self.putRaw(line)

    def putRaw(self, lines):
        """
        Insert a raw line into the buffer (use with caution)

        @param lines if lines is a list, insert every element into the buffer.
        If it's a single line, insert it into the buffer.
        """
        if type(lines) is list:
            for l in lines:
                self._buffer.append(l)
        else:
            self._buffer.append(lines)

    def makeLine(self, metric, tags, value, agg=None, agg_freq=10,
                 sample_rate=False, namespace=defaultNS, timestamp=None):
        """
        Generate a metric line

        @param metric Name metric such as "response_time"
        @param tags Tags to associate this value with, for example
        {from: 'serviceA', to: 'serviceB', method: 'login'}
        @param value
        @param agg List of aggregations to be applied by the Telemetron.
        Ex: ['avg', 'p90', 'min']
        @param agg_freq Aggregation frequency in seconds. One of: 10, 15, 30,
        60 or 300
        @param sample_rate Sampling rate (1-99)
        @param timestamp is the timestamp associated with the metric. If not
        set, will use current time (utc)

        @returns metric line string
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

        @param send_buffer_length if True, appends a metric to the buffer with
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
        @returns the current number of messages in buffer.
        """
        return len(self._buffer)

    def timeSinceFlush(self):
        """
        @returns elapsed time, in seconds, since last successful flush call
        """
        if self._lastFlush:
            return time.time() - self._lastFlush
        return 0



class AutoFlushClient(Client):
    """
    AutoFlushClient

    A version of Client that auto flushes when a specific buffer size is hit.
    """

    def __init__(self, flush_size=30, *args, **kws):
        """
        Constructor

        @param flush_size is the buffer size at which a flush should be
        triggered.
        """

        self.flushSize = flush_size
        self._doFlush = True

        super(AutoFlushClient, self).__init__(*args, **kws)


    def putRaw(self, lines):
        super(AutoFlushClient, self).putRaw(lines)

        #  Prevents an infinite method call loop
        if self._doFlush and self.bufferCount() >= self.flushSize:
            self._doFlush = False
            self.flush()
            self._doFlush = True
