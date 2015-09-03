from .base import MessageHandler

class Rot13Handler(MessageHandler):

  TRIGGERS = ['rot13', 'rot']
  HELP = 'apply ROT13 to the given text'

  def handle_message(self, event, triggers, query):
    return query.encode('rot13')
