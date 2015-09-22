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
Usage:
    serialization dump [options] [--path=<path>]
    serialization load [options] [preview] [--path=<path>]
    serialization clear
    serialization preview

Options:
    -p, --path=<path>           save or load path or filename[default: ./]
    -f, --format=<format>...    save format, "json" or "pickle"
                                [default: json pickle]
    -n, --name=<name>           save or dump filename without extension,
                                default is the same as this file
    -h, -?                      print usage
    --help                      print this message
    -v, --version               print the version'''

bashlog.stdoutlogger(logger=None, level=bashlog.DEBUG, color=True)
pie = Docpie(doc, version="Alpha")
dic = pie.convert_2_dict()
s = json.dumps(doc)
d = json.loads(s)
new_pie = pie.convert_2_docpie(d)

# print(pie.usages)

# pie.preview()

# try:
#     pie.docpie()
# except:
#     # print(get_exc_plus())
#     # sys.exit()
#     # print(pie.usages)
#     raise
# else:
#     print(pie)

# for each in p._chain:
#     print(each)
