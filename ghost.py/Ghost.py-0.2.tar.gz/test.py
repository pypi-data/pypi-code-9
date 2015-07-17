import logging
import sys
import gc
from ghost import Ghost


ghost = Ghost(log_level=logging.DEBUG)

session = ghost.start()

for i in xrange(0, 100):
    session.open('http://jeanphix.me')

ghost.exit()
