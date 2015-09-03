import fnmatch
import importlib
import logging
import os
import re

_handler_classes = set()
handlers = set()

class HandlerRegistry(type):

  def __init__(cls, name, bases, namespace):
    super(HandlerRegistry, cls).__init__(name, bases, namespace)
    _handler_classes.add(cls)
    _handler_classes.difference_update(bases)

class Handler(object):

  __metaclass__ = HandlerRegistry

  def __init__(self, client):
    self.client = client

  def handle(self, event):
    raise NotImplementedError

class MessageHandler(Handler):

  TRIGGER_ANCHOR = '^'
  TRIGGER_PREFIX = '!'
  TRIGGERS = []
  HELP = None

  def __init__(self, *args, **kwargs):
    super(MessageHandler, self).__init__(*args, **kwargs)
    pattern = '%s%s%s' % (
        r'^' if '^' in self.TRIGGER_ANCHOR else r'(?<!\w)',
        r'%s(?:%s)' % (self.TRIGGER_PREFIX, '|'.join(self.TRIGGERS)),
        r'$' if '$' in self.TRIGGER_ANCHOR else r'(?!\w)')
    self.TRIGGER_RE = re.compile(pattern, flags=re.IGNORECASE)

  def handle(self, event):
    if event['type'] == 'message' and 'subtype' not in event:
      triggers = self.TRIGGER_RE.findall(event['text'])
      if triggers:
        query = self.TRIGGER_RE.sub('', event['text']).strip()
        return self.handle_message(event, triggers, query)

  def handle_message(self, event, triggers, query):
    raise NotImplementedError

def init_handlers(client):
  handlers_dir = os.path.dirname(__file__)
  for filename in fnmatch.filter(os.listdir(handlers_dir), '[!_]*.py'):
    module = filename[:-3]
    try:
      importlib.import_module('..%s' % module, package=__name__)
      logging.info('loaded handler module: %s' % module)
    except Exception:
      logging.exception('failed to load handler module: %s' % module)

  for handler_class in _handler_classes:
    try:
      handler = handler_class(client)
      handlers.add(handler)
      logging.info('initialized handler: %s' % handler)
    except Exception:
      logging.exception('failed to initialize handler: %s' % handler_class)
      continue

    if isinstance(handler, MessageHandler):
      if not handler.TRIGGERS:
        logging.warning('message handler with no triggers: %s' % handler)
      if not handler.HELP:
        logging.warning('message handler with no help: %s' % handler)
