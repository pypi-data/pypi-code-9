import os
import unittest

from pyebnf.primitive import pprint as pprint_parser_tree
from pyebnf.parser import Parser, TokenType

from . import FIXTURES_ROOT


def flatten(c, p):
  return c.is_type(TokenType.expression) and p.is_type(TokenType.expression)


class ParserTestCase(unittest.TestCase):
  def test_parser(self):
    source = """expression = number , [operator , expression] ;
                number = ? get_digit ? ;
                (* a comment for you! *)
             """
    parser = Parser()
    grammar = parser.parse(source).trimmed().flattened().flattened(flatten)

    # pprint_parser_tree(grammar, source_len=len(source))

    self.assertEqual(list(c.node_type for c in grammar.children),
                     [TokenType.rule, TokenType.rule, TokenType.comment])

  def test_parser_2(self):
    with open(os.path.join(FIXTURES_ROOT, "ebnf.ebnf")) as rf:
      source = rf.read()

    parser = Parser()
    grammar = parser.parse(source).trimmed().flattened().flattened(flatten)

    # pprint_parser_tree(grammar, source_len=len(source))

    rules = {n.children[0].value for n in grammar.children if n.is_type(TokenType.rule)}
    expected = {"grammar", "comment", "rule", "identifier", "expression", "expression_terminal",
                "option_group", "repetition_group", "grouping_group", "special_handling", "number",
                "terminal", "operator", "op_mult", "op_add", "alpha_character", "digit",
                "printable"}
    self.assertEqual(rules & expected, expected)

  @unittest.skip
  def test_parser_scratch(self):
    source = """expression = number , [operator , expression] ;
                number = ? get_digit ? ;
                repeated = 3 * number ;
             """
    parser = Parser()
    grammar = parser.parse(source).trimmed().flattened().flattened(flatten)

    # pprint_parser_tree(grammar, source_len=len(source))
