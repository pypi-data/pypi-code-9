import os
import unittest

from pyebnf.primitive import pprint as pprint_parse_tree
from pyebnf.compiler import Compiler

from . import FIXTURES_ROOT


class CompilerTestCase(unittest.TestCase):
  def test_compiler(self):
    with open(os.path.join(FIXTURES_ROOT, "test.ebnf")) as rf:
      source = rf.read()

    compiler = Compiler(source)

    # pprint_parse_tree(compiler.grammar, source_len=len(source))
    # print(compiler.directives)

    output = compiler.output_source
    # print(output)
