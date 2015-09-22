import socket
import time
import logging
import random

"""
This class represents the telemetron Client.
It handles the socket connection to a telemetron server and has the
ability to construct metric lines.
"""
class Client:
    defaultNS = "application"

    TCP_SOCKET = "tcp"
    UDP_SOCKET = "udp"

    """
    Constructor.

    @param host is telemetron's server host or ip
    @param port is telemetron's server port
    @param prefix is the prefix string to use in metrics
    @param socket_type is either udp or tcp
    @param sample_rate is the sampling rate in percent 1 to 99
    @param start_socket if True, will call startSocket() immediately
    """
    def __init__(self, host="127.0.0.1", port=2013, prefix="client",
    socket_type="udp", sample_rate=100.0, start_socket=True):
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

    """
    Start the socket.
    If socket was already started, just connect to endpoint (in TCP mode).
    """
    def startSocket(self):
        if self.socketType.lower() == 'tcp':
            if self._socket is None:
                self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((self.host, self.port))
        elif self.socketType.lower() == 'udp':
            if self._socket is None:
                self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    """
    Close the socket
    """
    def closeSocket(self):
        self._socket.close()

    """
    Sends a timing metric

    @param name Name of the counter. Ex: response_time
    @param value
    @param tags Tags to associate this value with, for example {from: 'serviceA', to: 'serviceB', method: 'login'}
    @param agg List of aggregations to be applied by the Telemetron. Ex: ['avg', 'p90', 'min']
    @param aggFreq Aggregation frequency in seconds. One of: 10, 15, 30, 60 or 300
    @param namespace Define the metric namespace. Default: application
    """
    def time(self, name, value, tags={}, agg=['avg', 'p90', 'count', 'count_ps'],
    aggFreq=10, namespace=defaultNS):
        tags.update({"unit": 'ms'})
        self.put(
            'timer.%s' % (name,),
            tags,
            value | 0,
            agg,
            aggFreq,
            self.sampleRate,
            namespace)

    """
    Increments a counter

    @param name Name of the counter. Ex: transactions
    @param value
    @param tags Tags to associate this value with, for example {type: 'purchase_order'}
    @param agg List of aggregations to be applied by the Telemetron. Ex: ['avg', 'p90', 'min']
    @param aggFreq Aggregation frequency in seconds. One of: 10, 15, 30, 60 or 300
    @param namespace Define the metric namespace. Default: application
    """
    def inc(self, name, value, tags={}, agg=['sum', 'count', 'count_ps'],
    aggFreq=10, namespace=defaultNS):
        self.put('counter.%s' % (name,),
            tags,
            value | 0,
            agg,
            aggFreq,
            self.sampleRate,
            namespace)

    """
    Adds a Gauge

    @param name Name of the Gauge. Ex: current_sessions
    @param value
    @param tags Tags to associate this value with, for example {page: 'overview'}
    @param agg List of aggregations to be applied by the Telemetron. Ex: ['avg', 'p90', 'min']
    @param aggFreq Aggregation frequency in seconds. One of: 10, 15, 30, 60 or 300
    @param namespace Define the metric namespace. Default: application
    """
    def gauge(self, name, value, tags={}, agg=['last'], aggFreq=10,
    namespace=defaultNS):
        self.put('gauge.%s' % (name,),
            tags,
            value | 0,
            agg,
            aggFreq,
            self.sampleRate,
            namespace)

    """
    Adds a new metric to the in-memory buffer.

    @param metric Name metric such as "response_time"
    @param tags Tags to associate this value with, for example {from: 'serviceA', to: 'serviceB', method: 'login'}
    @param value
    @param agg List of aggregations to be applied by the Telemetron. Ex: ['avg', 'p90', 'min']
    @param aggFreq Aggregation frequency in seconds. One of: 10, 15, 30, 60 or 300
    @param sample_rate Sampling rate (1-99)
    """
    def put(self, metric, tags, value, agg=[], aggFreq=10, sample_rate=100.0,
    namespace=defaultNS):
        sample_rate_normalized = sample_rate / 100.0
        if random.random() <= sample_rate_normalized:
            line = self.makeLine(metric, tags, value, agg, aggFreq,
                sample_rate, namespace)
            self.putRaw(line)


    """
    Insert a raw line into the buffer (use with caution)
    """
    def putRaw(self, line):
        self._buffer.append(line)

    """
    Generate a metric line

    @param metric Name metric such as "response_time"
    @param tags Tags to associate this value with, for example {from: 'serviceA', to: 'serviceB', method: 'login'}
    @param value
    @param agg List of aggregations to be applied by the Telemetron. Ex: ['avg', 'p90', 'min']
    @param aggFreq Aggregation frequency in seconds. One of: 10, 15, 30, 60 or 300
    @param sample_rate Sampling rate (1-99)

    @returns metric line string
    """
    def makeLine(self, metric, tags, value, agg=[], aggFreq=10,
    sample_rate=False, namespace=defaultNS):
        def c(prev, tag):
            return "%s,%s=%s" % (prev, tag, tags[tag])

        metricName = "%s.%s.%s" % (self.prefix, namespace, metric)
        line = reduce(c, tags, metricName)
        line += " %s %d" % (value, time.time())
        if len(agg) > 0 and aggFreq:
            aggCopy = list(agg)
            aggCopy.append(aggFreq)
            line += " %s" % (','.join([str(a) for a in aggCopy]),)
            if sample_rate:
                line += " %s" % (sample_rate,)
        return line

    """
    Flush buffer to socket

    @param send_buffer_length if True, appends a metric to the buffer with
        the current buffer length

    """
    def flush(self, send_buffer_length=True):
        if len(self._buffer) > 0:
            if send_buffer_length:
                self.put('buffer.flush_length',
                    {},
                    len(self._buffer),
                    ['avg'])
            message = "%s\n" % ("\n".join( self._buffer ), )
            if self.socketType.lower() == 'tcp':
                self._socket.sendall(message)
            elif self.socketType.lower() == 'udp':
                self._socket.sendto(message, (self.host, self.port))
            self._buffer = []
            self._lastFlush = time.time()


    """
    Return the current number of messages in buffer.
    """
    def bufferCount(self):
        return len(self._buffer)

    """
    Return elapsed time, in seconds, since last successful flush call
    """
    def timeSinceFlush(self):
        if self._lastFlush:
            return (time.time() - self._lastFlush)
        return 0
