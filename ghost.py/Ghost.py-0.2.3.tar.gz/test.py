import logging
import sys
import gc
from ghost import Ghost


ghost = Ghost(log_level=logging.DEBUG)


for i in xrange(0, 100):
    with ghost.start() as session:
        session.open('http://jeanphix.me')

ghost.exit()
