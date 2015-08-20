"""this module implement the basic web transaction metric

"""

import logging
import time
import sys
import traceback

from tingyun.api.tracert.database_node import DatabaseNode
from tingyun.api.transaction.transaction_cache import transaction_cache
from tingyun.api.tracert.tansaction_node import TransactionNode
from tingyun.api.tracert.error_node import ErrorNode
from tingyun.api.platform import six
import tingyun.api.tracert.time_trace


_logger = logging.getLogger(__name__)


class Transaction(object):
    """used to represent a web request transaction action

    """
    def __init__(self, proxy, enabled=None, framework="Python"):
        """
        :param proxy: application proxy instance
        :return:
        """
        self.framework = framework
        self.proxy = proxy
        self.enabled = False

        self.thread_id = transaction_cache().current_thread_id()
        self._transaction_id = id(self)
        
        self.background_task = False
        self.start_time = 0
        self.end_time = 0
        self.trace_node = []

        self._errors = []
        self._custom_params = {}
        self._slow_sql_nodes = []

        self.request_uri = None
        self.http_status = 500
        self.request_params = {}
        self._priority = 0
        self._group = None
        self._name = None
        self.apdex = 0
        self._frozen_path = None

        self.stack_trace_count = 0
        self.explain_plan_count = 0

        self.thread_name = "Unknown"
        self.referer = ""

        # set the global switch of agent.  the return application settings is download from server witch is merged
        # with the local settings on server
        # agent always be enabled if enabled in local settings. just not upload data when disabled by server.
        global_settings = proxy.global_settings
        if global_settings.enabled:
            if enabled or (enabled is None and proxy.enabled):
                self._settings = proxy.settings
                if not self._settings:
                    self.proxy.activate()
                    self._settings = proxy.settings

                if self._settings:
                    self.enabled = True

    def __enter__(self):
        """
        :return:
        """
        if not self.enabled:
            return self

        try:
            self.save_transaction()
        except Exception as _:
            _logger.fatal("Fatal error when save transaction. if this continues. please contact us for further \
                           investigation")
            raise
        
        self.start_time = time.time()
        self.trace_node.append(tingyun.api.tracert.time_trace.TimeTrace(None))

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        if not self.enabled:
            return

        try:
            self.drop_transaction()
        except Exception as err:
            _logger.fatal("Agent suffered fatal error when drop transaction. please contact us for further \
                           investigation")
            _logger.exception("error detail %s", err)
            raise

        if not self.is_uri_captured(self.request_uri):
            _logger.debug("ignore the uri %s", self.request_uri)
            return

        if exc_type is not None and exc_val is not None and exc_tb is not None:
            self.record_exception(exc_type, exc_val, exc_tb)
        
        self.end_time = time.time()
        duration = int((self.end_time - self.start_time) * 1000)
        root_node = self.trace_node.pop()
        children = root_node.children
        exclusive = duration + root_node.exclusive

        transaction_type = "WebAction" if not self.background_task else "BackgroundAction"
        group = self._group or ("Python" if self.background_task else "Uri")
        request_params = self.filter_params(self.request_params)
        uri = self.url_encode(self.request_uri)

        # replace the specified metric apdex_t
        apdex_t = self._settings.apdex_t
        path = self.path
        if path in self._settings.action_apdex:
            apdex_t = self._settings.action_apdex.get(path)

        node = TransactionNode(type=transaction_type, group=group, name=self._name, start_time=self.start_time,
                               end_time=self.end_time, request_uri=uri, duration=duration, thread_name=self.thread_name,
                               http_status=self.http_status, exclusive=exclusive, children=tuple(children),
                               path=self.path, errors=self._errors, apdex_t=apdex_t,
                               custom_params=self._custom_params, request_params=request_params,
                               referer=self.referer, slow_sql=self._slow_sql_nodes)

        self.proxy.record_transaction(node)

    def record_exception(self, exc=None, value=None, tb=None, params=None, transaction_type="WebAction",
                         ignore_errors=[]):
        """ record the exception for trace
        :param exc:
        :return:
        """
        if not self._settings.error_collector.enabled:
            return

        if exc is None and value is None and tb is None:
            exc, value, tb = sys.exc_info()

        if exc is None or value is None or tb is None:
            _logger.warning("None exception is got. skip it now. %s, %s, %s", exc, value, tb)
            return

        if self.http_status in self._settings.error_collector.ignored_status_codes:
            _logger.debug("ignore the status code %s", self.http_status)
            return

        # 'True' - ignore the error.
        # 'False'- record the error.
        # ignore status code and maximum error number filter will be done in data engine because of voiding repeat count
        # method ignore_errors() is used to detect the the status code which is can not captured
        if callable(ignore_errors):
            should_ignore = ignore_errors(exc, value, tb, self._settings.error_collector.ignored_status_codes)
            if should_ignore:
                return

        # think more about error occurred before deal the status code.
        if self.http_status in self._settings.error_collector.ignored_status_codes:
            _logger.debug("record_exception: ignore  error collector status code")
            return

        module = value.__class__.__module__
        name = value.__class__.__name__
        fullname = '%s:%s' % (module, name) if module else name

        request_params = self.filter_params(self.request_params)
        if params:
            custom_params = dict(request_params)
            custom_params.update(params)
        else:
            custom_params = dict(request_params)

        try:
            message = str(value)
        except Exception as _:
            try:
                # Assume JSON encoding can handle unicode.
                message = six.text_type(value)
            except Exception as _:
                message = '<unprintable %s object>' % type(value).__name__

        stack_trace = traceback.extract_tb(tb)
        node = ErrorNode(error_time=int(time.time()), http_status=self.http_status, error_class_name=fullname,
                         uri=self.url_encode(self.request_uri), thread_name=self.thread_name, message=message,
                         stack_trace=stack_trace, request_params=custom_params, transaction_type=transaction_type,
                         referer=self.referer)

        self._errors.append(node)

    @property
    def path(self):
        """the call tree path
        """
        if self._frozen_path:
            return self._frozen_path

        transaction_type = "WebAction" if not self.background_task else "BackgroundAction"
        name = self._name or "Undefined"

        if not self._settings.auto_action_naming:
            path = "%s/%s/%s" % (transaction_type, self.framework, self.url_encode(self.request_uri))
        else:
            path = '%s/%s/%s' % (transaction_type, self.framework, name)

        return path

    def url_encode(self, uri):
        """
        :param uri:
        :return:
        """
        encoded_url = "index"
        if not uri or uri == "/":
            return encoded_url

        # drop the uri first /
        uri = uri.replace('/', '', 1)
        encoded_url = uri.replace("/", "%2F")

        return encoded_url

    def free_path(self):
        if self._frozen_path is None:
            self._priority = None

            self._frozen_path = self.path

            self.apdex = None
    
    def set_transaction_name(self, name, group="Function", priority=None):
        """used to consist metric identification
        """
        if self._priority is None:
            return

        if priority is not None and priority < self._priority:
            return

        if isinstance(name, bytes):
            name = name.decode('Latin-1')
        
        self._priority = priority
        self._group = group
        self._name = name
        
    def save_transaction(self):
        transaction_cache().save_transaction(self)
    
    def drop_transaction(self):
        transaction_cache().drop_transaction(self)

    def process_database_node(self, node):
        """record the database node
        :param node: database node
        :return:
        """
        if type(node) is not DatabaseNode:
            return

        if not self._settings.action_tracer.enabled:
            return

        if not self._settings.action_tracer.slow_sql:
            return

        if self._settings.action_tracer.record_sql == 'off':
            return

        if node.duration < self._settings.action_tracer.slow_sql_threshold:
            return

        self._slow_sql_nodes.append(node)

    def push_node(self, node):
        self.trace_node.append(node)
        
    def pop_node(self, node):
        """return parent trace node
        """
        last = self.trace_node.pop()
        assert last == node
        parent = self.trace_node[-1]

        return parent
    
    def current_node(self):
        """
        """
        if self.trace_node:
            return self.trace_node[-1]

    def is_uri_captured(self, uri):
        """check the uri is captured or not
        :param uri: uri of the request
        :return: True, if it's need to captured. else return False
        """
        # capture all url
        if not self._settings.urls_captured:
            return True

        for p in self._settings.urls_captured:
            if p and p.match(uri):
                return True

        return False

    def filter_params(self, params):
        """filter the parameters
        :param params: the dict parameters
        :return: filtered parameters
        """
        result = {}

        if not params:
            return result

        if not self._settings.action_tracer.enabled or not self._settings.capture_params:
            return result

        for key in params:
            if key not in self._settings.ignored_params:
                result[key] = params[key]

        return result

    @property
    def name(self):
        return self._name

    @property
    def group(self):
        return self._group

    @property
    def settings(self):
        return self._settings


def current_transaction():
    """return current transaction in the thread
    :return:
    """
    return transaction_cache().current_transaction()
