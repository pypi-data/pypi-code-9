import unittest
from functools import partial

import pyebnf.primitive as P


class PrimitiveTestCase(unittest.TestCase):
  def test_get_terminal(self):
    node1 = next(P.get_terminal("a", "abc"))
    self.assertEqual(node1.node_type, P.NodeType.terminal)
    self.assertEqual(len(node1.children), 1)
    self.assertEqual(node1.value, "a")
    self.assertEqual(node1.consumed, 1)

    node2 = next(P.get_terminal("bc", "bcde"))
    self.assertEqual(node2.node_type, P.NodeType.terminal)
    self.assertEqual(len(node2.children), 1)
    self.assertEqual(node2.value, "bc")
    self.assertEqual(node2.consumed, 2)

    with self.assertRaises(P.DeadEnd):
      next(P.get_terminal("b", "abc"))

  def test_get_concatenation(self):
    extractors = [P.terminal("a"),
                  P.terminal("b"),
                  P.terminal("c")]
    node1 = next(P.get_concatenation(extractors, True, "  a b   c def"))

    self.assertEqual(node1.node_type, P.NodeType.concatenation)
    self.assertEqual(len(node1.children), 3)
    self.assertEqual([c.value for c in node1.children], ["a", "b", "c"])
    self.assertEqual(node1.consumed, 9)

    with self.assertRaises(P.DeadEnd):
      next(P.get_concatenation(extractors, True, "abdefc"))

  def test_get_concatenation2(self):
    gen = P.concatenation([P.terminal("a"), P.terminal("b"), P.alternation([P.terminal("cd"), P.terminal("cde")])])
    candidates = gen("abcde")
    alts = []
    while True:
      try:
        alts.append(next(candidates))
      except (StopIteration, P.DeadEnd):
        break
    self.assertEqual(2, len(alts))

  def test_get_alternation(self):
    extractors = [P.terminal("a"),
                  P.terminal("bc"),
                  P.terminal("b")]
    alternation = P.get_alternation(extractors, "bc  b abc")
    node1 = next(alternation)

    self.assertEqual(node1.node_type, P.NodeType.terminal)
    self.assertEqual(node1.value, "bc")
    self.assertEqual(node1.consumed, 2)

    node2 = next(alternation)
    self.assertEqual(node2.node_type, P.NodeType.terminal)
    self.assertEqual(node2.value, "b")
    self.assertEqual(node2.consumed, 1)

    with self.assertRaises(P.DeadEnd):
      next(alternation)

  def test_get_optional_repetition(self):
    extractor = P.get_concatenation([
      P.terminal("("),
      P.option(
        P.concatenation([
          P.terminal("a"),
          P.repetition(
            P.concatenation([
              P.terminal(","),
              P.terminal("a")
            ])
          )
        ])
      ),
      P.terminal(")")
    ], True, "()")
    next(extractor)

  def test_get_repetition(self):
    extractor1 = P.terminal("a")
    node1 = next(P.get_repetition(extractor1, "aaaa", bound=3))

    self.assertEqual(node1.node_type, P.NodeType.repetition)
    self.assertEqual(len(node1.children), 3)
    self.assertEqual([c.value for c in node1.children], ["a", "a", "a"])
    self.assertEqual(node1.consumed, 3)

    node2 = next(P.get_repetition(extractor1, "aaaaab"))
    self.assertEqual(node2.node_type, P.NodeType.repetition)
    self.assertEqual(len(node2.children), 5)
    self.assertEqual(node2.consumed, 5)

    with self.assertRaises(P.DeadEnd):
      next(P.get_repetition(extractor1, "ab", bound=2))

    extractor2 = P.alternation([P.terminal("a"), P.terminal("b")])

    node2 = next(P.get_repetition(extractor2, "abaabbbacde"))
    self.assertEqual(len(node2.children), 8)
    self.assertEqual(
      [c.value for c in node2.children],
      ["a", "b", "a", "a", "b", "b", "b", "a"])
    self.assertEqual(node2.consumed, 8)

  def test_get_option(self):
    extractors = [P.terminal("a"),
                  P.terminal("bc")]
    alternator = P.alternation(extractors)

    node1 = next(P.get_option(alternator, "a"))
    self.assertEqual(node1.node_type, P.NodeType.option)
    self.assertEqual(len(node1.children), 1)
    self.assertEqual(node1.consumed, 1)

    node2 = next(P.get_option(alternator, "bc"))
    self.assertEqual(node2.node_type, P.NodeType.option)
    self.assertEqual(len(node2.children), 1)
    self.assertEqual(node2.consumed, 2)

    node3 = next(P.get_option(alternator, "c"))
    self.assertEqual(node3.node_type, P.NodeType.option)
    self.assertEqual(len(node3.children), 0)
    self.assertEqual(node3.consumed, 0)

  def test_get_exclusion(self):
    extractors = [P.terminal(str(n)) for n in range(10)]
    get_digit = P.alternation(extractors)
    get_zero = P.terminal("0")

    node1 = next(P.get_exclusion(get_digit, get_zero, "10"))
    self.assertEqual(node1.node_type, P.NodeType.terminal)
    self.assertEqual(node1.value, "1")

    with self.assertRaises(P.DeadEnd):
      next(P.get_exclusion(get_digit, get_zero, "01"))

  def test_composition(self):
    # Model:
    # number = ( digit - "0" , { digit } | "0" ) , [ "." , digit , { digit } ] , ";";

    digit = lambda: P.alternation([P.terminal(str(n)) for n in range(10)])
    non_zero_digit = lambda: P.exclusion(digit(), P.terminal("0"))
    digits = lambda: P.repetition(digit())

    number = lambda: P.concatenation(
      [P.alternation(
        [P.concatenation(
          [non_zero_digit(),
           digits()]),
         P.terminal("0")]),
       P.option(
        P.concatenation(
          [P.terminal("."),
           digit(),
           digits()])),
       P.terminal(";")])

    tokenize = lambda text: next(number()(text)).reconstruct()

    self.assertEqual(tokenize("123.4;"), "123.4;")
    self.assertEqual(tokenize("1234;"), "1234;")
    self.assertEqual(tokenize("0.5;"), "0.5;")

    with self.assertRaises(P.DeadEnd): tokenize("0123;")
    with self.assertRaises(P.DeadEnd): tokenize("123.;")
    with self.assertRaises(P.DeadEnd): tokenize(".5;")
    with self.assertRaises(P.DeadEnd): tokenize("abc;")

  # @unittest.skip
  def test_recursion(self):
    digit = lambda: P.alternation([P.terminal(str(n)) for n in range(10)])
    number = lambda text: P.Node.iterate_reduce("number", P.concatenation([digit(), P.repetition(digit())]), text)
    operator = lambda text: P.Node.iterate_reduce("operator", P.alternation([P.terminal(n) for n in ["+", "-", "*", "/", "⨉"]]), text)
    statement = lambda text: P.Node.iterate_merge("statement", P.concatenation([expression, P.terminal(";")]), text)
    subexpression = lambda text: P.Node.iterate_merge("subexpr", P.concatenation([P.terminal("("), expression, P.terminal(")")]), text)

    def unskipped(parts, skip):
      if skip is None:
        return parts
      else:
        return list(p for i, p in enumerate(parts) if i not in skip)

    def skipped(extractor, skip):
      return partial(extractor, skip=skip)

    def expression(text, *, skip=None):
      recursives = {2, 3, 4, 5}

      parts = [number,
               subexpression,
               P.concatenation([expression, operator, expression]),
               # # # # #
               # P.concatenation([skipped(expression, recursives), P.terminal("+"), expression]),
               # P.concatenation([skipped(expression, recursives), P.terminal("-"), expression]),
               # P.concatenation([skipped(expression, recursives), P.terminal("⨉"), expression]),
               # P.concatenation([skipped(expression, recursives), P.terminal("/"), expression]),
              ]
      gen = P.alternation(unskipped(parts, skip))

      yield from P.Node.iterate_merge("expr", gen, text)

    # print()
    eqm = "(8-5)⨉3/(20+5)"
    eq = eqm + ";"
    tree = next(statement(eq))
    # P.pprint(tree)
    self.assertEqual(tree.reconstruct(include_ignored=False), eq)

