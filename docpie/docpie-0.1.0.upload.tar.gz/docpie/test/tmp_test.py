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
from docpie.token import Argv
from docpie.error import DocpieExit
from docpie.tracemore import get_exc_plus
from docopt import docopt

__doc__ = '''
        Usage: prog [options]
                    [--repeat=<sth> --repeat=<sth>]
'''

bashlog.stdoutlogger(logger=None, level=bashlog.DEBUG, color=True)
pie = Docpie(__doc__)

# print(pie.usages)

# pie.preview()

try:
    pie.docpie()
except:
    # print(get_exc_plus())
    # sys.exit()
    # print(pie.usages)
    raise
else:
    print(pie)

# for each in p._chain:
#     print(each)
