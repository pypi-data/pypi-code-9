import unittest

from pyebnf.exception import OperatorError
from pyebnf.operator import Operator, OperatorNode, OptreeNode, infix_to_postfix, postfix_to_optree


ADD = Operator("+", 1)
SUB = Operator("-", 1)
MUL = Operator("*", 2)
DIV = Operator("/", 2)


def _opnode(op):
  return OperatorNode(op, 0)


class OperatorTestCase(unittest.TestCase):
  def test_infix_to_postfix(self):
    a = _opnode(ADD)
    s = _opnode(SUB)
    m = _opnode(MUL)

    nodes0 = [3, a, 5, s, 8]
    self.assertEqual(infix_to_postfix(nodes0), [3, 5, a, 8, s])

    nodes1 = [3, a, 5, m, 8]
    self.assertEqual(infix_to_postfix(nodes1), [3, 5, 8, m, a])

  def test_postfix_to_optree(self):
    a = _opnode(ADD)
    s = _opnode(SUB)
    m = _opnode(MUL)

    nodes0 = [3, 5, 8, m, a]
    root = postfix_to_optree(nodes0)

    self.assertEqual(root.opnode, a)
    l0, r0 = root.operands

    self.assertIsInstance(r0, OptreeNode)
    self.assertEqual(r0.opnode, m)
    r0l, r0r = r0.operands
    self.assertEqual(r0l, 5)
    self.assertEqual(r0r, 8)

    self.assertEqual(l0, 3)

    with self.assertRaises(OperatorError):
      postfix_to_optree([3, 5, 8])

    with self.assertRaises(OperatorError):
      postfix_to_optree([3, 5, 8, m, a, s])

    with self.assertRaises(OperatorError):
      postfix_to_optree([m])
