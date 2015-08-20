import cgi
import logging
import threading

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

from tingyun.api.transaction.base import Transaction


_logger = logging.getLogger(__name__)


class WebTransaction(Transaction):
    """
    """
    def __init__(self, application, environ, framework="Python"):
        """
        """
        Transaction.__init__(self, application, environ, framework)

        self.get_thread_name()
        script_name = environ.get('SCRIPT_NAME', "")
        path_info = environ.get('PATH_INFO', "")
        self.request_uri = environ.get("REQUEST_URI", "")
        self.referer = environ.get("HTTP_REFERER", "")

        if self.request_uri:
            self.request_uri = urlparse.urlparse(self.request_uri)[2]
            
        if script_name or path_info:
            if not path_info:
                path = script_name
            elif not script_name:
                path = path_info
            else:
                path = script_name + path_info

            self.set_transaction_name(path, 'Uri', priority=1)

            if not self.request_uri:
                self.request_uri = path
        else:
            if self.request_uri:
                self.set_transaction_name(self.request_uri, 'Uri', priority=1)

        # get the param
        self._get_request_params(environ)

    def deal_response(self, status, response_headers, *args):
        """
        :param status:
        :param response_headers:
        :param args:
        :return:
        """
        try:
            self.http_status = int(status.split(' ')[0])
        except Exception as _:
            _logger.warning("get status code failed, status is %s", status)

    def _get_request_params(self, environ):
        """
        :param environ: cgi environment
        :return: referer
        """
        value = environ.get('QUERY_STRING', "")
        if value:
            params = {}

            try:
                params = urlparse.parse_qs(value, keep_blank_values=True)
            except Exception:
                try:
                    # method <parse_qs> only for backward compatibility,  method <parse_qs> new in python2.6
                    params = cgi.parse_qs(value, keep_blank_values=True)
                except Exception:
                    pass

            self.request_params.update(params)

    def get_thread_name(self):
        """
        :return: thread name
        """
        try:
            self.thread_name = threading.currentThread().getName()
        except Exception as err:
            _logger.info("Get thread name failed. %s", err)
            self.thread_name = "unknown"

        return self.thread_name
