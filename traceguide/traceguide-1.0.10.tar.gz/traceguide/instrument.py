""" This is the official Traceguide Instrumentation for Python.

:class:`~Runtime` is the primary class and can be utilized to report logs
and operations to Traceguide.

:class:`~ActiveSpan` objects are created by the Runtime to store span info.
TraceJoinIds such as 'end_user_id' can be added to ActiveSpan objects.
"""
from thrift import Thrift

from atexit import register
import threading, jsonpickle, random, time, sys
from socket import error as socket_error

from traceguide.crouton import ttypes
from traceguide import constants, util, connection as conn

# Runtime Singleton
_singleton_runtime = None
_singleton_mutex = threading.Lock()

def get_runtime(group_name='', access_token='', secure=True,
                service_host="api.traceguide.io", service_port=9997,
                debugger=None):
    """ Return singleton instance of the Runtime.

        :param str group_name: name identifying the type of service that
            is being tracked
        :param str access_token: project's access token
        :param bool secure: whether HTTP connection is secure
        :param str service_host: Traceguide server host
        :param int service_port: Traceguide server port

        On the first call to get_runtime provide the listed parameters in order
        to instantiate and return the singleton. After the first call, all
        parameters will ignored and the singleton will be returned.

        Note: debugger parameter is for internal testing purposes only.
    """
    global _singleton_runtime
    with _singleton_mutex:
        if _singleton_runtime is None:
            _singleton_runtime = Runtime(group_name, access_token, secure,
                                         service_host, service_port, debugger)
        return _singleton_runtime

def initialize(group_name='', access_token='', secure=True,
               service_host="api.traceguide.io", service_port=9997,
               debugger=None):
    """ Initializes the default runtime

        All calls after the first successful call to this function will be
        ignored.
    """
    get_runtime(group_name, access_token, secure, service_host, service_port, debugger)

def span(name):
    """ Calls span() on the default runtime.
    """
    return get_runtime().span(name)

def infof(fmt, *args, **kwargs):
    """ Calls infof() on the default runtime.
    """
    parsed = util._parse_level_log_kwargs(**kwargs)
    get_runtime()._level_log(constants.INFO_LOG, parsed.get(constants.PAYLOAD),
                             parsed.get(constants.SPAN_GUID), fmt, args)

def warnf(fmt, *args, **kwargs):
    """ Calls warnf() on the default runtime.
    """
    parsed = util._parse_level_log_kwargs(**kwargs)
    get_runtime()._level_log(constants.WARN_LOG, parsed.get(constants.PAYLOAD),
                             parsed.get(constants.SPAN_GUID), fmt, args)

def errorf(fmt, *args, **kwargs):
    """ Calls errorf() on the default runtime.
    """
    parsed = util._parse_level_log_kwargs(**kwargs)
    get_runtime()._level_log(constants.ERR_LOG, parsed.get(constants.PAYLOAD),
                             parsed.get(constants.SPAN_GUID), fmt, args)

def fatalf(fmt, *args, **kwargs):
    """ Calls fatalf() on the default runtime.
    """
    parsed = util._parse_level_log_kwargs(**kwargs)
    get_runtime()._level_log(constants.FATAL_LOG, parsed.get(constants.PAYLOAD),
                             parsed.get(constants.SPAN_GUID), fmt, args)

def flush():
    """ Calls flush() on the default runtime.
    """
    get_runtime().flush()


class Runtime(object):
    """ Instances of Runtime are used to sends logs and spans to the server.

        :param str group_name: name identifying the type of service that
            is being tracked
        :param str access_token: project's access token
        :param bool secure: whether HTTP connection is secure
        :param str service_host: Traceguide server host
        :param int service_port: Traceguide server port

        Note: debugger parameter is for internal testing purposes only.
    """
    def __init__(self, group_name, access_token,
                 secure=True, service_host="api.traceguide.io",
                 service_port=9997, debugger=None):
        # Thrift runtime configuration
        guid = util._generate_guid()
        timestamp = util._now_micros()
        self._runtime = ttypes.Runtime(guid, timestamp, group_name)
        self._service_url = util._service_url_from_hostport(secure,
                                                            service_host,
                                                            service_port)
        self._auth = ttypes.Auth(access_token)
        self._mutex = threading.Lock()
        self._log_records, self._span_records = ([] for i in range(2))

        # Only establish timer-based flush if no debugger is provided
        self._debugger = debugger
        self._connection = conn._Connection(self._service_url)
        self._connection._open()
        self._event = threading.Event()
        self._flush_thread = threading.Thread(target=self._timed_flush,
                                              name=constants.FLUSH_THREAD_NAME)
        self._flush_thread.daemon = True
        if self._debugger is None:
            self._flush_thread.start()

        # Configuration for clean up & runtime disabling
        register(self.shutdown)
        self._disabled_runtime = False

    def shutdown(self):
        """ Shutdown the Runtime's connection by flushing the remaining
            logs and spans and then disabling the Runtime.

            Note: spans and logs will no longer be reported after shutdown
            is called.
        """
        if self._disabled_runtime:
            return
        self.flush()
        self.disable()

    def disable(self):
        """ Disable the Runtime, such that all calls to the Runtime API
            become no-ops.

            Note: spans and logs will no longer be reported to after disable
            is called.
        """
        # Note: Closing connection twice results in an error. Exit early
        #       if runtime has already been disabled.
        if self._disabled_runtime:
            return
        with self._mutex:
            self._event.set()
            self._connection._close()
            self._disabled_runtime = True
            self._log_records = None
            self._span_records = None

    def infof(self, fmt, *args, **kwargs):
        """ Log with Info Level.

            :param str fmt: log statement with formatting, e.g. 'log from %s'
            :param args: args for formatted string
            :param payload: optional payload
            :param span_guid: optional span_guid to associate log with a span
        """
        parsed = util._parse_level_log_kwargs(**kwargs)
        self._level_log(constants.INFO_LOG, parsed.get(constants.PAYLOAD),
                        parsed.get(constants.SPAN_GUID), fmt, args)

    def warnf(self, fmt, *args, **kwargs):
        """ Log with Warning Level.

            :param str fmt: log statement with formatting, e.g. 'log from %s'
            :param args: args for formatted string
            :param payload: optional payload
            :param span_guid: optional span_guid to associate log with a span
        """
        parsed = util._parse_level_log_kwargs(**kwargs)
        self._level_log(constants.WARN_LOG, parsed.get(constants.PAYLOAD),
                        parsed.get(constants.SPAN_GUID), fmt, args)

    def errorf(self, fmt, *args, **kwargs):
        """ Log with Error Level.

            :param str fmt: log statement with formatting, e.g. 'log from %s'
            :param args: args for formatted string
            :param payload: optional payload
            :param span_guid: optional span_guid to associate log with a span
        """
        parsed = util._parse_level_log_kwargs(**kwargs)
        self._level_log(constants.ERR_LOG, parsed.get(constants.PAYLOAD),
                        parsed.get(constants.SPAN_GUID), fmt, args)

    def fatalf(self, fmt, *args, **kwargs):
        """ Log with Fatal Level. Leads to program termination.

            :param str fmt: log statement with formatting, e.g. 'log from %s'
            :param args: args for formatted string
            :param payload: optional payload
            :param span_guid: optional span_guid to associate log with a span
        """
        parsed = util._parse_level_log_kwargs(**kwargs)
        fmt_str = self._level_log(constants.FATAL_LOG,
                                  parsed.get(constants.PAYLOAD),
                                  parsed.get(constants.SPAN_GUID), fmt, args)
        sys.exit(fmt_str)

    def log(self, log_statement, payload=None, level=None, span_guid=None):
        """ Record a log statement with optional payload and importance level.

            :param str logStatement: log text
            :param payload: an string, int, object, etc. whose serialization
                will be sent to the server
            :param str span_guid: associate the log with a specifc span
                operation by providing a span_guid
            :param char level: for internal use only
                importance level of log - 'I' info, 'W' warning, 'E' error,
                'F' fatal
        """
        if self._disabled_runtime:
            return
        timestamp = util._now_micros()
        guid = self._runtime.guid
        log_record = ttypes.LogRecord(timestamp, guid, message=log_statement,
                                      level=level, span_guid=span_guid)

        if payload is not None:
            try:
                log_record.payload_json = \
                    jsonpickle.encode(payload, constants.JSON_UNPICKLABLE,
                                      max_depth=constants.JSON_MAX_DEPTH)
            except:
                log_record.payload_json = jsonpickle.encode(constants.JSON_FAIL)

        self._add_log(log_record)


    def span(self, name):
        """ Mark the start of a span operation

            :param str name: the name by which the recording span can
                be identified
            :return: ActiveSpan that references the newly initialized span
            :rtype: ActiveSpan
        """
        if self._disabled_runtime:
            return ActiveSpan(None, None)
        span_guid = util._generate_guid()
        runtime_guid = self._runtime.guid
        timestamp = util._now_micros()
        join_ids = []
        span_record = ttypes.SpanRecord(span_guid, runtime_guid, name, join_ids,
                                        timestamp)
        return ActiveSpan(self, span_record)

    def flush(self):
        """ Send unreported data to the server.

            Every few seconds automatic reports are sent to the server.
            However, one can also manually send reports to the server.
            Calling flush() will ensure that any current unreported data
            will be immediately sent to the host server.
        """
        if self._disabled_runtime:
            return
        if self._debugger is None:
            connection = conn._Connection(self._service_url)
            connection._open()
            self._flush_worker(connection)
            connection._close()
        else:
            self._debug_flush()

    def _timed_flush(self):
        """ Send scheduled report requests to the server.
        """
        while not self._event.isSet():
            if not self._connection._initial_connection_established:
                self._connection._open()
            if self._connection._initial_connection_established:
                time.sleep(constants.FLUSH_PERIOD_SECS)
                self._flush_worker(self._connection)

    def _flush_worker(self, connection):
        """ Use the given connection to transmit the current logs and spans
            as a report request.
        """
        if connection._initial_connection_established:
            report_request = self._construct_report_request()
            try:
                resp = connection._client.Report(self._auth, report_request)
                if resp.commands is None:
                    return
                for command in resp.commands:
                    if command.disable:
                        self.disable()
            except Thrift.TException:
                self._store_on_disconnect(report_request)
            except socket_error:
                self._store_on_disconnect(report_request)

    def _construct_report_request(self):
        """ Construct a report request.
        """
        with self._mutex:
            report = ttypes.ReportRequest(self._runtime, self._span_records,
                                          self._log_records)
            self._span_records = []
            self._log_records = []
            return report

    def _level_log(self, level, payload, span_guid, fmt, *args):
        """ Logging with levels.
        """
        if self._disabled_runtime:
            return
        try:
            # Since the args are passed down from an encapsulating package
            # they are packaged within a tuple so that args is a tuple of
            # n values within a tuple. To extract the tuple of n values select
            # the first element of the encapsulating tuple.
            fmt_str = fmt % args[0]
        except TypeError:
            fmt_str = ':'.join(['[INVALID FORMAT STRING]', fmt])

        self.log(fmt_str, payload, level, span_guid)
        return fmt_str

    def _add_log(self, log):
        """ Safely add a log to the buffer. Throw out logs if the limit has
            been reached.
        """
        with self._mutex:
            if len(self._log_records) is constants.MAX_LOGS:
                delete_index = random.randint(0, constants.MAX_LOGS - 1)
                self._log_records[delete_index] = log
            else:
                self._log_records.append(log)

    def _add_span(self, span):
        """ Safely add a span to the buffer. Throw out spans if the liit has
            been reached.
        """
        with self._mutex:
            if len(self._span_records) is constants.MAX_SPANS:
                delete_index = random.randint(0, constants.MAX_SPANS - 1)
                self._span_records[delete_index] = span
            else:
                self._span_records.append(span)

    def _store_on_disconnect(self, report_request):
        """ Store logs and the spans from a report request in the runtime's
            buffers.
        """
        for log in report_request.log_records:
            self._add_log(log)
        for span in report_request.span_records:
            self._add_span(span)

    def _debug_flush(self):
        """ Send report request to debugger.
        """
        report_request = self._construct_report_request()
        self._debugger.Report(report_request)

class ActiveSpan(object):
    """ Wrapper class for thrift span_record.

        Can also be used as a context manager, like so:
        >>> with instrument.span("subsystem/my_operation) as span:
        ...   span.add_join_id(...)
    """
    def __init__(self, runtime, span_record):
        self._runtime = runtime
        self._span_record = span_record
        if span_record is not None:
            self.span_guid = span_record.span_guid
        else:
            self.span_guid = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self.errorf('Uncaught exception thrown in span: %s, %s', exc_type, exc_value)
        self.end()
        return False  # A True would suppress the exeception

    def add_join_id(self, key, val):
        """ Add a JoinID to the active span.

            :param str key: type of id, for example 'end_user_id'
            :param str value: id, for example 'John'
        """
        if self._runtime is None:
            return
        if self._span_record is None:
            return
        trace_join_id = ttypes.TraceJoinId(key, val)
        self._span_record.join_ids.append(trace_join_id)

    def end(self):
        """ End the active span so that it can be reported to the server

            :return: whether span recording successfully ended
            :rtype: bool
        """
        if self._runtime is None:
            return False
        if self._span_record is None:
            return False
        self._span_record.youngest_micros = util._now_micros()
        self._runtime._add_span(self._span_record)
        return True

    def infof(self, fmt, *args, **kwargs):
        """ Log with Info Level. Log is sent attached to the span.

            :param str fmt: log statement with formatting, i.e. 'log from %s'
            :param args: args for formatted string
            :param payload: optional payload
        """
        parsed = util._parse_level_log_kwargs(**kwargs)
        self._runtime._level_log(constants.INFO_LOG,
                                 parsed.get(constants.PAYLOAD),
                                 self.span_guid, fmt, args)

    def warnf(self, fmt, *args, **kwargs):
        """ Log with Warning Level. Log is sent attached to the span.

            :param str fmt: log statement with formatting, i.e. 'log from %s'
            :param args: args for formatted string
            :param payload: optional payload
        """
        parsed = util._parse_level_log_kwargs(**kwargs)
        self._runtime._level_log(constants.WARN_LOG,
                                 parsed.get(constants.PAYLOAD),
                                 self.span_guid, fmt, args)

    def errorf(self, fmt, *args, **kwargs):
        """ Log with Error Level. Log is sent attached to the span.

            :param str fmt: log statement with formatting, i.e. 'log from %s'
            :param args: args for formatted string
            :param payload: optional payload

        """
        parsed = util._parse_level_log_kwargs(**kwargs)
        self._runtime._level_log(constants.ERR_LOG,
                                 parsed.get(constants.PAYLOAD),
                                 self.span_guid, fmt, args)

    def fatalf(self, fmt, *args, **kwargs):
        """ Log with Fatal Level. Leads to program termination.
            Log is sent attached to the span.

            :param str fmt: log statement with formatting, i.e. 'log from %s'
            :param args: args for formatted string
            :param payload: optional payload
        """
        parsed = util._parse_level_log_kwargs(**kwargs)
        fmt_str = self._runtime._level_log(constants.FATAL_LOG,
                                           parsed.get(constants.PAYLOAD),
                                           self.span_guid, fmt, args)
        sys.exit(fmt_str)

