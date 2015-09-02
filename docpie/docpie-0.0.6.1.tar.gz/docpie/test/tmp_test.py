import unittest
import logging
import sys
import json
import difflib
from pprint import pprint

from docpie.tracemore import get_exc_plus
from docpie import docpie, Docpie
from docpie import bashlog
from docpie.parser import UsageParser, OptionParser, Parser
from docpie.element import *
from docpie.tokens import Argv
from docpie.saver import Saver
from docpie.error import DocpieExit
from docpie.tracemore import get_exc_plus
from docopt import docopt


__doc__ = """
Usage: pie.py [command] [--option] [<argument>]
"""


bashlog.stdoutlogger(logger=None, level=bashlog.DEBUG, color=True)

sys.argv = 'prog --option command arg'.split()

pie = Docpie(__doc__)
# pie.preview()

try:
    pie.docpie()
except:
    # print(get_exc_plus())
    # sys.exit()
    raise
else:
    print(pie)

# for each in p._chain:
#     print(each)
