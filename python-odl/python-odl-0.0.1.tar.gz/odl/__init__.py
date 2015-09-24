# Set default logging handler to avoid "No handler found" warnings.
import logging
import logging.config

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

log = logging.getLogger(__name__)
try:
    logging.config.fileConfig('settings/logging.conf')
except:
    pass

log.addHandler(NullHandler())
