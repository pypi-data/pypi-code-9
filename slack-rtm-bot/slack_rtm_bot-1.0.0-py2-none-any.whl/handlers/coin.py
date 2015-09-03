from collections import Counter
import random

from .base import MessageHandler
from ..util import parse_int

class CoinHandler(MessageHandler):

  TRIGGERS = ['coin', 'flip']
  HELP = 'flip the given number of coins; default 1'

  def handle_message(self, event, triggers, query):
    times = parse_int(query, default=1)
    flips_gen = (random.choice(('heads', 'tails')) for _ in xrange(times))
    if times > 10:
      counter = Counter(flips_gen)
      return '%s heads, %s tails' % (counter['heads'], counter['tails'])
    else:
      return ', '.join(flips_gen)
