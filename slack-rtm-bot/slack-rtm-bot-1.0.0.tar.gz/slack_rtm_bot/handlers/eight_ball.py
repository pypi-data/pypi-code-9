import random

from .base import MessageHandler

class EightBallHandler(MessageHandler):

  TRIGGERS = ['8ball', 'eight_ball']
  HELP = 'random fortune'

  def handle_message(self, event, triggers, query):
    return random.choice((
        'It is certain',
        'It is decidedly so',
        'Without a doubt',
        'Yes - definitely',
        'You may rely on it',
        'As I see it, yes',
        'Most likely',
        'Outlook good',
        'Yes',
        'Signs point to yes',
        'Reply hazy, try again',
        'Ask again later',
        'Better not tell you now',
        'Cannot predict now',
        'Concentrate and ask again',
        "Don't count on it",
        'My reply is no',
        'My sources say no',
        'Outlook not so good',
        'Very doubtful',
    ))
