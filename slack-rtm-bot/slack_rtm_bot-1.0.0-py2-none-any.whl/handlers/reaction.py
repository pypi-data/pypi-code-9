from .base import MessageHandler
from .. import settings

class ReactionHandler(MessageHandler):

  TRIGGER_ANCHOR = ''
  TRIGGER_PREFIX = ''
  TRIGGERS = sorted(settings.EMOJI_REACTIONS.keys())
  HELP = 'add emoji reactions'

  def handle_message(self, event, triggers, query):
    for trigger in triggers:
      trigger = trigger.lower()
      if trigger in settings.EMOJI_REACTIONS:
        self.client.api_call(
            'reactions.add',
            name=settings.EMOJI_REACTIONS[trigger],
            channel=event['channel'],
            timestamp=event['ts'])
