import unittest

import pyebnf.primitive as P


class ParseNodeTestCase(unittest.TestCase):
  def test_init(self):
    n0 = P.ParseNode("abc")
    self.assertEqual(n0.node_type, "abc")
    self.assertEqual(n0.children, tuple())
    self.assertEqual(n0.consumed, 0)
    self.assertIsNone(n0.position)

    n1 = P.ParseNode(None, children=[P.ParseNode(None, children=["a"], consumed=1)])
    self.assertEqual(n1.consumed, 1)

  def test_position(self):
    n0 = P.ParseNode(None, position=3)
    self.assertEqual(n0.position, 3)

    n1 = P.ParseNode(None, children=[P.ParseNode(None, position=1)])
    self.assertEqual(n1.position, 1)

    n2 = P.ParseNode(None)
    self.assertIsNone(n2.position)

  def test_is_empty(self):
    n0 = P.ParseNode(None)
    self.assertTrue(n0.is_empty)

    n1 = P.ParseNode(None, children=["a"], consumed=1)
    self.assertFalse(n1.is_empty)

    n2 = P.ParseNode(None, children=[P.ParseNode(None)])
    self.assertTrue(n2.is_empty)

  def test_is_value(self):
    n0 = P.ParseNode(None, children=["a"], consumed=1)
    self.assertTrue(n0.is_value)

    n1 = P.ParseNode(None)
    self.assertFalse(n1.is_value)

    n2 = P.ParseNode(None, children=[P.ParseNode(None, children=["a"], consumed=1)])
    self.assertFalse(n2.is_value)

  def test_value(self):
    n0 = P.ParseNode(None, children=["a"], consumed=1)
    self.assertEqual(n0.value, "a")

  def test_svalue(self):
    n0 = P.ParseNode(None, children=[" a\t\n"], consumed=4)
    self.assertEqual(n0.svalue, "a")

  def test_add_ignored(self):
    n0 = P.ParseNode(None, children=["a"], consumed=1)
    n0.add_ignored(" ")
    self.assertEqual(n0.ignored, " ")
    self.assertEqual(n0.consumed, 2)

  def test_flattened(self):
    n0 = P.ParseNode("A",
                     children=[P.ParseNode("B",
                                           children=[P.ParseNode("C", children=["a"], consumed=1, position=5),
                                                     P.ParseNode("C", children=["b"], consumed=1),
                                                     P.ParseNode("C", children=["c"], consumed=1)])])
    n1 = n0.flattened(lambda c, p: True)
    self.assertEqual(len(n1.children), 3)
    self.assertEqual(n1.children, ("a", "b", "c"))
    self.assertEqual(n1.position, 5)

  def test_trimmed(self):
    n0 = P.ParseNode("A", children=[P.ParseNode("B", children=["a"], consumed=1, position=8),
                                    P.ParseNode(P.ParseNodeType.terminal, children=["a"], consumed=1)])
    n1 = n0.trimmed()
    self.assertEqual(len(n1.children), 1)

  def test_merge(self):
    n0 = P.ParseNode("A", children=[P.ParseNode("B", children=["b"], consumed=1)])
    n1 = P.ParseNode("C", children=[P.ParseNode("B", children=["c"], consumed=1)])
    n2 = n0 << n1
    self.assertEqual(n2.node_type, n0.node_type)
    self.assertEqual(len(n2.children), len(n0.children) + len(n1.children))
    self.assertEqual(n2.consumed, n0.consumed + n1.consumed)

  def test_retyped(self):
    n0 = P.ParseNode("A", children=[P.ParseNode("B", children=["b"], consumed=1, ignored=" ")])
    n1 = n0.retyped("C")
    self.assertEqual(n1.node_type, "C")
    self.assertEqual(len(n0.children), len(n1.children))
    self.assertEqual(n0.children[0].value, n1.children[0].value)

  def test_compressed(self):
    ignored = "    "
    position = 39

    n0 = P.ParseNode("Number",
                     children=[P.ParseNode("Digit",
                                           children=["8"],
                                           consumed=5,
                                           ignored=ignored,
                                           position=position),
                               P.ParseNode("Digit", children=["3"], consumed=1),
                               P.ParseNode("Digit", children=["0"], consumed=1)])
    n1 = n0.compressed(include_ignored=False)
    self.assertTrue(n1.is_value)
    self.assertEqual(n1.position, position)
    self.assertEqual(n1.consumed, 7)
    self.assertEqual(n1.ignored, ignored)
    self.assertEqual(n1.value, "830")

    n2 = n0.compressed(include_ignored=True)
    self.assertTrue(n2.consumed, 7)
    self.assertIsNone(n2.ignored)
    self.assertEqual(n2.value, ignored + "830")

  def test_len(self):
    n0 = P.ParseNode(None, children=["a"], consumed=1)
    self.assertEqual(len(n0), 1)

    n1 = P.ParseNode(None, children=[P.ParseNode(None, children=["a"], consumed=1),
                                      P.ParseNode(None, children=["b"], consumed=1)])
    self.assertEqual(len(n1), 2)


class PrimitiveTestCase(unittest.TestCase):
  def test_terminal(self):
    e0 = P.terminal("a")
    t0 = "abc"
    n0 = e0(t0)

    self.assertEqual(n0.node_type, P.ParseNodeType.terminal)
    self.assertTrue(n0.is_value)
    self.assertEqual(n0.value, "a")
    self.assertEqual(n0.position, -len(t0))
    self.assertEqual(len(n0.children), 1)
    self.assertEqual(n0.children[0], "a")

    t1 = "bcd"
    with self.assertRaises(P.DeadEnd):
      e0(t1)

  def test_concatenation(self):
    c0 = P.concatenation(["a", "b", "c"], ignore_whitespace=True)
    t0 = "abc"
    n0 = c0(t0)

    self.assertEqual(n0.node_type, P.ParseNodeType.concatenation)
    self.assertFalse(n0.is_value)
    self.assertEqual(n0.position, -len(t0))
    self.assertEqual(len(n0.children), 3)
    self.assertEqual(len(n0), 3)

    with self.assertRaises(P.DeadEnd):
      c0("bcd")

    t1 = """ a\tb\nc"""
    n1 = c0(t1)
    # The position excludes skipped whitespace.
    self.assertEqual(n1.position, -len(t1) + 1)
    self.assertEqual(len(n1), 3)
    self.assertEqual(n1.consumed, 6)

    c1 = P.concatenation(["a", "b", "c"], ignore_whitespace=False)
    n2 = c1(t0)
    self.assertEqual(len(n2.children), 3)

    # c1 raises on t1 because t1 has whitespace but c1 doesn't ignore whitespace.
    with self.assertRaises(P.DeadEnd):
      c1(t1)

  def test_alternation(self):
    c0 = P.alternation(["a", "b", "c", "a("])

    self.assertEqual(c0("agh").value, "a")
    self.assertEqual(c0("b(").value, "b")
    self.assertEqual(c0("c_-").value, "c")
    self.assertEqual(c0("a(b, c)").value, "a(")

    with self.assertRaises(P.DeadEnd):
      c0("d")

  def test_option(self):
    c0 = P.option("a")

    n0 = c0("a")
    self.assertEqual(n0.node_type, P.ParseNodeType.repetition)
    self.assertEqual(len(n0.children), 1)
    self.assertEqual(n0.children[0].value, "a")
    self.assertFalse(n0.is_empty)

    n1 = c0("b")
    self.assertEqual(n1.node_type, P.ParseNodeType.repetition)
    self.assertTrue(n1.is_empty)

  def test_zero_or_more(self):
    c0 = P.zero_or_more("a")

    n0 = c0("ab")
    self.assertEqual(n0.node_type, P.ParseNodeType.repetition)
    self.assertEqual(len(n0.children), 1)

    n1 = c0("aaaaa")
    self.assertEqual(len(n1.children), 5)

    n2 = c0("ba")
    self.assertTrue(n2.is_empty)

  def test_one_or_more(self):
    c0 = P.one_or_more("a")

    n0 = c0("ab")
    self.assertEqual(n0.node_type, P.ParseNodeType.repetition)
    self.assertEqual(len(n0.children), 1)

    n1 = c0("aaa")
    self.assertEqual(len(n1.children), 3)

    with self.assertRaises(P.DeadEnd):
      c0("baa")

  def test_repeated(self):
    c0 = P.repeated("a", 3)

    n0 = c0("aaa")
    self.assertEqual(n0.node_type, P.ParseNodeType.repetition)
    self.assertEqual(len(n0.children), 3)

    n1 = c0("aaaaaa")
    self.assertEqual(len(n0.children), 3)

    with self.assertRaises(P.DeadEnd):
      c0("aa")

  def test_repetition(self):
    c0 = P.repetition("a", (2, 4))

    with self.assertRaises(P.DeadEnd):
      c0("a")

    n0 = c0("aa")
    self.assertEqual(n0.node_type, P.ParseNodeType.repetition)
    self.assertEqual(len(n0.children), 2)

    self.assertEqual(len(c0("aaa").children), 3)
    self.assertEqual(len(c0("aaaa").children), 4)
    self.assertEqual(len(c0("aaaaa").children), 5)

    with self.assertRaises(P.DeadEnd):
      c0("b")

  def test_exclusion(self):
    c0 = P.alternation(["a", "b"])
    c1 = P.exclusion(c0, "b")

    n0 = c1("a")
    self.assertEqual(n0.node_type, P.ParseNodeType.terminal)
    self.assertEqual(n0.value, "a")

    self.assertEqual(c0("b").value, "b")

    with self.assertRaises(P.DeadEnd):
      c1("ba")

  def test_optional_repetition(self):
    # Makes sure nested repetitions will terminate.
    c0 = P.zero_or_more(P.option(P.alternation(["a", "b"])))
    t0 = "ababaabbaaab"
    n0 = c0(t0)

    self.assertEqual(n0.consumed, len(t0))
