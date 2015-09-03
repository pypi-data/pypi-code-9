
from salesmachine.version import VERSION
from salesmachine.client import Client

__version__ = VERSION

"""Settings."""
key = "fWlU0N6jJKbcgW_OR6OidQ"
secret = "UZ8YjpEXXPBYmROvPnJ5jw"
on_error = None
debug = False
send = True

default_client = None

def set_contact(*args, **kwargs):
  """
  Send a set_contact request
  """
  _proxy('set_contact', *args, **kwargs)

def set_account(*args, **kwargs):
  """
  Send a set_account request
  """
  _proxy('set_account', *args, **kwargs)

def track_event(*args, **kwargs):
  """
  Send a track_event request
  """
  _proxy('track_event', *args, **kwargs)

def track_pageview(*args, **kwargs):
  """
  Send a track_pageview request
  """
  _proxy('track_pageview', *args, **kwargs)

def flush():
    """Tell the client to flush."""
    _proxy('flush')

def join():
    """Block program until the client clears the queue"""
    _proxy('join')

def _proxy(method, *args, **kwargs):
    """Create an salesmachine client if one doesn't exist and send to it."""
    global default_client
    if not default_client:
        default_client = Client(key, secret, debug=debug, on_error=on_error,
                                send=send)

    fn = getattr(default_client, method)
    fn(*args, **kwargs)
