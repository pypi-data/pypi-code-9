"""ohh - CLI tool for OHH project"""

from ohh.runner import Runner

DEFAULT_CONFIG = {
    'endpoint': 'https://ohh-api.claudetech.com',
    'token': 'None',
    'cpu_threshold': '0',
}


class OhhError(Exception):
    def __init__(self, message):
        self.message = message


__version__ = '0.5.0'
__author__ = 'Daniel Perez <daniel@claudetech.com>'
__all__ = []
