"""Contains the Operator namedtuple and several methods for working with it."""

from collections import namedtuple
from enum import Enum

from .exception import OperatorError


class Association(Enum):
  """Association direction enum for operators."""
  left = 1
  right = 2


Operator = namedtuple("Operator", ["symbol", "precedence", "association", "cardinality"])
Operator.__new__.__defaults__ = (Association.left, 2)
OptreeNode = namedtuple("OptreeNode", ["opnode", "operands", "type"])
OptreeNode.__new__.__defaults__ = (None, )
OperatorNode = namedtuple("OperatorNode", ["operator", "position"])


def infix_to_postfix(nodes, *, recurse_types=None):
  """Convert a list of nodes in infix order to a list of nodes in postfix order.

  E.G. with normal algebraic precedence, 3 + 4 * 5 -> 3 4 5 * +
  """
  output = []
  operators = []

  for node in nodes:
    if isinstance(node, OperatorNode):
      # Drain out all operators whose precedence is gte the node's...
      cmp_operator = node.operator
      while operators:
        current_operator = operators[-1].operator
        if current_operator.precedence > cmp_operator.precedence or \
           current_operator.precedence == cmp_operator.precedence and current_operator.association == Association.left:
          output.append(operators.pop())
        else:
          break
      operators.append(node)
    else:
      if recurse_types is not None and node.node_type in recurse_types:
        output.extend(infix_to_postfix(node.children, recurse_types=recurse_types))
      else:
        output.append(node)

  return output + list(reversed(operators))


def postfix_to_optree(nodes):
  """Convert a list of nodes in postfix order to an Optree."""
  while len(nodes) > 1:
    nodes = _reduce(nodes)

  if len(nodes) == 0:
    raise OperatorError("Empty node list")

  node = nodes[0]

  if isinstance(node, OperatorNode):
    raise OperatorError("Operator without operands")

  if isinstance(node, OptreeNode):
    return node

  return OptreeNode(None, (node, ))


def infix_to_optree(nodes, *, recurse_types=None):
  """Convert a list of nodes in infix order to an Optree."""
  return postfix_to_optree(infix_to_postfix(nodes, recurse_types=recurse_types))


def _reduce(nodes):
  """Finds the first operator in the list, converts it and its operands to a OptreeNode, then
  returns a new list with the operator and operands replaced by the new OptreeNode.
  """
  i = 0
  while i < len(nodes):
    if isinstance(nodes[i], OperatorNode):
      break
    else:
      i += 1

  if i == len(nodes):
    raise OperatorError("No operator found")

  operator_node = nodes[i]
  operator = operator_node.operator
  operands_lbound = i - operator.cardinality

  if operands_lbound < 0:
    raise OperatorError("Insufficient operands for operator {0}".format(operator.symbol))

  return nodes[:operands_lbound] + \
         [OptreeNode(operator_node, tuple(nodes[operands_lbound:i]))] + \
         nodes[i+1:]


def pprint(root, depth=0, space_unit="    "):
  """Pretty print an optree, starting at root."""
  spacing = space_unit * depth

  if isinstance(root, OptreeNode):
    print("{0}Operator ({1})".format(spacing, root.opnode.operator.symbol if root.opnode else "None -> IDENTITY"))
    for operand in root.operands:
      pprint(operand, depth + 1)
  else:
    print("{0}• {1}".format(spacing, root))

