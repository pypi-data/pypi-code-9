import os
import unittest

from pyebnf.primitive import pprint
from pyebnf.compiler import compile_grammar, split_source
from pyebnf.parser import Parser
from . import FIXTURES_ROOT


class CompilerTestCase(unittest.TestCase):
  def test_compiler(self):
    with open(os.path.join(FIXTURES_ROOT, "simple_lang.ebnf")) as rf:
      ebnf_text = rf.read()
    content, directives, comments = split_source(ebnf_text)

    parser = Parser()
    grammar = parser.parse(content)
    # pprint(grammar)
    # print(compile_grammar(grammar, directives=directives))
