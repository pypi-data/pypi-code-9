import logging
import time

from slackclient import SlackClient

from . import settings
from .handlers.base import handlers, init_handlers

def get_responses(event):
  for handler in handlers:
    try:
      yield handler.handle(event)
    except Exception:
      logging.exception('handler failed to handle event: %s' % handler)

def run_bot(client):
  while True:
    logging.debug('rtm_read')
    for event in client.rtm_read():
      if 'ok' in event:
        if event['ok']:
          logging.debug('response confirmation: %s' % event['reply_to'])
        else:
          logging.error('bad response confirmation: %s' % event)
        continue

      logging.info('event: %s' % event['type'])
      response = '\n'.join(filter(None, get_responses(event)))
      if response:
        logging.info('response: %s' % response)
        client.rtm_send_message(event['channel'], response)

    time.sleep(settings.READ_INTERVAL_SECONDS)

def main():
  logging.basicConfig(filename=settings.LOG_FILE,
                      format=settings.LOG_FORMAT,
                      level=settings.LOG_LEVEL)

  client = SlackClient(settings.API_TOKEN)
  logging.info('rtm_connect')
  if not client.rtm_connect():
    logging.critical('failed to connect')
    return

  init_handlers(client)
  run_bot(client)

if __name__ == '__main__':
  main()
