import requests

from .base import MessageHandler
from ..util import parse_int

_XKCD_API_CURRENT_URL = 'http://xkcd.com/info.0.json'
_XKCD_URL_TEMPLATE = 'http://xkcd.com/%s/'

class XkcdHandler(MessageHandler):

  TRIGGERS = ['xkcd']
  HELP = 'link to the given xkcd comic; default current'

  def handle_message(self, event, triggers, query):
    number = parse_int(query)
    if not number:
      response = requests.get(_XKCD_API_CURRENT_URL)
      response.raise_for_status()
      number = response.json()['num']
    return _XKCD_URL_TEMPLATE % number
