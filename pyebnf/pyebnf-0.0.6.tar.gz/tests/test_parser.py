import os
import unittest

from pyebnf.primitive import Node, NodeType, pprint as pprint_node_tree
from pyebnf.parser import Parser, TokenType
from pyebnf.operator import Operator, infix_to_postfix
from pyebnf.util import to_line_and_char

from . import FIXTURES_ROOT


class ParserTestCase(unittest.TestCase):
  def test_parser(self):
    with open(os.path.join(FIXTURES_ROOT, "simple_lang.ebnf")) as rf:
      ebnf_text = rf.read()
    parser = Parser()
    grammar = parser.parse(ebnf_text)

    # print()
    # pprint_node_tree(grammar)

    for child in grammar.children:
      self.assertEqual(child.node_type, TokenType.rule)
      name, assignment, expression, terminator = child.children
      self.assertEqual(name.node_type, TokenType.identifier)
      self.assertEqual(assignment.node_type, NodeType.terminal)
      self.assertEqual(assignment.value, "=")
      self.assertEqual(expression.node_type, TokenType.expression)
      self.assertEqual(terminator.node_type, NodeType.terminal)
      self.assertEqual(terminator.value, ";")
