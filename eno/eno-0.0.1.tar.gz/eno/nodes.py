"""Abstraction of a remote eno hardware node."""


class Node(object):
  """Representation of a remote eno hardware node.

  This class is used on the testing machine to control a remote eno node.  The
  hardware itself does not use this class, it instead uses the control server.
  """

  def __init__(self):
    self.ip_address = ''
    self.sim = ''
    self.phone_number = ''

  def sms(self, phone_number, message):
    """Send an SMS."""

  def call(self, phone_number, **kwargs):
    """Make a call.

    Args:
      phone_number: the number to call

    Kwargs:
      hangup: whether to hangup immediately after the call is answered (default
              is True)
    """

  def hangup(self):
    """Terminates any ongoing call."""

  def data(self, target):
    """Use data services.

    Args:
      target: will send an HTTP GET to this address
    """

  def wait_for_activity(self, activity, **kwargs):
    """Block until some activity completes.

    This could mean waiting until an SMS is received, waiting until a call is
    received or blocking until data is returned from a website.

    Args:
      activity: one of sms, call or data

    Kwargs:
      body: blocks until an SMS with this particular message is received
      sender: blocks until a call from this number is received
      target: blocks until data from this target is received
      timeout: the max amount of time to block (default: 10s)
    """

  def get_log(self, activity):
    """Gets info from an activity log.

    Args:
      activity: one of sms, call or data
    """

  def reset_log(self, activity):
    """Resets an activity log.

    Args:
      activity: one of sms, call or data
    """


def get_node(name):
  """Shortcut method to get an eno node's data.

  Args:
    name: the name of the node

  Returns a Node instance.
  """
