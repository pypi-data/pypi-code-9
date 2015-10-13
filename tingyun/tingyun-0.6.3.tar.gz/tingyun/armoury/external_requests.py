
"""this module is defined to detect the requests module
"""

from tingyun.armoury.ammunition.external_tracker import wrap_external_trace


def detect_requests_request(module):
    """
    :param module:
    :return:
    """
    def request_url(method, url, *args, **kwargs):
        """
        """
        return url

    wrap_external_trace(module, 'request', 'requests', request_url)


def detect_requests_sessions(module):
    """
    :param module:
    :return:
    """
    def request_url(instance, method, url, *args, **kwargs):
        """
        """
        return url

    wrap_external_trace(module, 'Session.request', 'requests', request_url)
