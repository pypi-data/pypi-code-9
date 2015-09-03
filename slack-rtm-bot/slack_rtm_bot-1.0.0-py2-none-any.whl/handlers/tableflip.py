# -*- coding: utf-8 -*-

from .base import MessageHandler

class TableFlipHandler(MessageHandler):

  TRIGGER_ANCHOR = ''
  TRIGGER_PREFIX = ''
  TRIGGERS = ['tableflip']
  HELP = 'flip a table'

  def handle_message(self, event, triggers, query):
    return '(╯°□°)╯︵ ┻━┻'
