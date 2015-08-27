"""Abstraction of a remote eno hardware node."""

import os
import time

import requests
import yaml


class Node(object):
  """Representation of a remote eno hardware node.

  This class is used on the testing machine to control a remote eno node.  The
  hardware itself does not use this class, it instead uses the control server.
  """

  def __init__(self, **kwargs):
    self.name = kwargs.pop('name', '')
    self.ip_address = kwargs.pop('ip_address', '')
    self.port = kwargs.pop('port', '5000')
    self.sim = kwargs.pop('sim', '')
    self.phone_number = kwargs.pop('phone_number', '')
    self.server_address = '%s:%s' % (self.ip_address, self.port)

  def sms(self, phone_number, message):
    """Send an SMS."""
    data = {
      'phone_number': phone_number,
      'message': message,
    }
    endpoint = '%s/sms' % self.server_address
    response = requests.post(endpoint, data=data)
    if response.status_code != 200:
      raise ValueError

  def call(self, phone_number, **kwargs):
    """Make a call.

    Args:
      phone_number: the number to call

    Kwargs:
      hangup_immediately: whether to hangup immediately after the call is
                          answered (default is True)
    """
    hangup_immediately = kwargs.get('hangup_immediately', True)
    data = {
      'phone_number': phone_number,
      'hangup_immediately': hangup_immediately,
    }
    endpoint = '%s/call' % self.server_address
    response = requests.post(endpoint, data=data)
    if response.status_code != 200:
      raise ValueError

  def hangup(self):
    """Terminates any ongoing call."""
    endpoint = '%s/hangup' % self.server_address
    response = requests.post(endpoint)
    if response.status_code != 200:
      raise ValueError

  def data(self, target):
    """Use data services.

    Args:
      target: will send an HTTP GET to this address
    """
    data = {
      'target': target,
    }
    endpoint = '%s/data' % self.server_address
    response = requests.post(endpoint, data=data)
    if response.status_code != 200:
      raise ValueError

  def wait_for_activity(self, activity, **kwargs):
    """Block until some activity completes.

    This could mean waiting until an SMS is received, waiting until a call is
    received or blocking until data is returned from a website.

    Args:
      activity: one of sms, call or data

    Kwargs:
      text: blocks until an SMS with this particular text is received
      sender: blocks until a call from this number is received
      target: blocks until data from this target is received
      timeout: the max amount of time to block (default: 10s)
    """
    timeout = kwargs.pop('timeout', 10)
    if activity not in ('sms', 'call', 'data'):
      raise ValueError
    if activity == 'sms':
      # Block until the SMS log has a new entry, or until 10s have elapsed.
      start_time = time.time()
      start_log_size = len(self.get_log('sms'))
      while True:
        new_log_size = len(self.get_log('sms'))
        if new_log_size > start_log_size:
          break
        elif time.time() > start_time + timeout:
          break
        time.sleep(1)

  def get_log(self, activity):
    """Gets info from an activity log.

    Args:
      activity: one of sms, call or data
    """
    if activity not in ('sms', 'call', 'data'):
      raise ValueError
    endpoint = '%s/log/%s' % (self.server_address, activity)
    response = requests.get(endpoint)
    if response.status_code != 200:
      raise ValueError
    return response.json()['messages']

  def reset_log(self, activity):
    """Resets an activity log.

    Args:
      activity: one of sms, call or data
    """
    if activity not in ('sms', 'call', 'data'):
      raise ValueError
    endpoint = '%s/log/%s' % (self.server_address, activity)
    response = requests.delete(endpoint)
    if response.status_code != 200:
      raise ValueError


def get_node(name):
  """Shortcut method to get an eno node's data.

  Args:
    name: the name of the node

  Returns a Node instance.
  """
  with open(os.path.expanduser('~/.enorc')) as config_file:
    config_data = yaml.load(config_file.read())
  # Verify that the requested name is actually in the config file.
  names = [n['name'] for n in config_data]
  if name not in names:
    raise ValueError
  # Instantiate a Node.
  for node_data in config_data:
    if name != node_data['name']:
      continue
    # The phone_number and port keys are optional and may not appear in the
    # config file.
    phone_number = ''
    if 'phone_number' in node_data:
      phone_number = node_data['phone_number']
    port = ''
    if 'port' in node_data:
      port = node_data['port']
    node = Node(
      name=name,
      ip_address=node_data['ip_address'],
      port=port,
      sim=node_data['sim'],
      phone_number=phone_number,
    )
    return node
