from .base import MessageHandler

class PingHandler(MessageHandler):

  TRIGGERS = ['ping']
  HELP = 'pong'

  def handle_message(self, event, triggers, query):
    return 'pong'
