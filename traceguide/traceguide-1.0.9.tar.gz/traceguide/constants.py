""" Constants for traceguide.instrument package.
"""

# traceguide_runtime constants
FLUSH_THREAD_NAME = 'Flush Thread'
FLUSH_PERIOD_SECS = 2.5
MAX_LOGS = 1000
MAX_SPANS = 1000

# Log Keywords
PAYLOAD = 'payload'
SPAN_GUID = 'span_guid'

# Log Levels
INFO_LOG = 'I'
WARN_LOG = 'W'
ERR_LOG = 'E'
FATAL_LOG = 'F'

# JSON pickle settings
JSON_FAIL = '<Invalid Payload'
JSON_MAX_DEPTH = 32
JSON_UNPICKLABLE = True
JSON_WARNING = True

# utils constants
SECONDS_TO_MICRO = 1000000
