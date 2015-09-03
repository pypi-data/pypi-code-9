from collections import Counter
import random

from .base import MessageHandler
from ..util import parse_int

class DiceHandler(MessageHandler):

  TRIGGERS = ['dice', 'roll']
  HELP = 'roll the given number of dice; default 1'

  def handle_message(self, event, triggers, query):
    times = parse_int(query, default=1)
    dice_gen = (random.randrange(1, 7) for _ in xrange(times))
    if times > 10:
      counter = Counter(dice_gen)
      return ', '.join('%s: %s' % (k, counter[k]) for k in xrange(1, 7))
    else:
      return ', '.join(map(str, dice_gen))
