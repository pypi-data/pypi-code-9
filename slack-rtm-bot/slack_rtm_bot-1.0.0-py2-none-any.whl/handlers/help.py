import re

from .base import handlers, MessageHandler

class HelpHandler(MessageHandler):

  TRIGGERS = ['help']
  HELP = 'help for the given command; default all commands'

  _RESPONSES = None

  def handle_message(self, event, triggers, query):
    if self._RESPONSES is None:
      self._init_responses()

    parts = []
    for trigger in re.findall(r'\w+', query.lower()):
      if trigger in self._RESPONSES:
        response = self._RESPONSES[trigger]
        if response not in parts:
          parts.append(response)

    return '```%s```' % ('\n'.join(parts) if parts else self._RESPONSES[None])

  def _init_responses(self):
    self._RESPONSES = {}

    for handler in handlers:
      if handler.TRIGGERS and handler.HELP:
        triggers = ', '.join('%s%s' % (
            handler.TRIGGER_PREFIX, trigger) for trigger in handler.TRIGGERS)
        for trigger in handler.TRIGGERS:
          self._RESPONSES[trigger] = '%s - %s' % (triggers, handler.HELP)

    self._RESPONSES[None] = '\n'.join(sorted(set(self._RESPONSES.values())))
