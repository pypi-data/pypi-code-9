"""This module contains classes and methods for working with the PXP Abstract Syntax Tree (AST)."""

from decimal import Decimal

from pyebnf.operator import OptreeNode


def pprint(node, depth=0, indent="    "):
  """Print out a PXP AST in a "pretty" way."""
  spacing = indent * depth

  if isinstance(node, ASTLeaf):
    print("{0}{1}".format(spacing, node))
  elif isinstance(node, OptreeNode):
    opnode = node.opnode
    if opnode:
      op = opnode.operator
      print("{0}Operator({1}, {2})".format(spacing, op.symbol, node.type))
    else:
      print("{0}Operator(None -> Identity)".format(spacing))
    for operand in node.operands:
      pprint(operand, depth + 1, indent)
  else:
    print("{0}{1}:".format(spacing, node.__class__.__name__))
    for child in node.children:
      pprint(child, depth + 1, indent)


class ASTNodeBase(object):
  """Base class for all AST Nodes."""
  def __init__(self, coords):
    """Construct an ASTNodeBase instance."""
    self.coords = coords

  def to_tuple(self):
    """Returns a tuple representing the node that can be understood by the PXP interpreter."""
    raise NotImplementedError()


class ASTNode(ASTNodeBase):
  """Base class for AST grouping nodes. A grouping node has children, as compared to leaf (value)
  nodes, which contains just a value.
  """
  def __init__(self, coords=None):
    """Construct an ASTNode instance."""
    super().__init__(coords)

  @property
  def children(self):
    """The children of the Node."""
    raise StopIteration()


class ASTLeaf(ASTNodeBase):
  """Base class for AST leaf nodes. Leaf nodes do not have children of their own, but rather
  represent leaves of the AST.
  """
  def __init__(self, value, type, coords=None):
    """Construct an ASTNode instance."""
    super().__init__(coords)
    self.value = value
    self.type = type

  def __repr__(self):
    """Returns a representation of the Node, including its type and value."""
    return "{0}({1})".format(self.__class__.__name__, self.value)

  def __str__(self):
    """Returns a string representation of the Node."""
    return repr(self)

  def to_tuple(self):
    """Returns a tuple representing the node that can be understood by the PXP interpreter."""
    return ("val", self.type, str(self.value))


class Program(ASTNode):
  """The Program (root) node of the AST."""
  def __init__(self, coords, statements):
    """Construct a Program node."""
    super().__init__(coords)
    self.statements = statements

  @property
  def children(self):
    """The statements that make up the program."""
    yield from self.statements

  def to_tuple(self):
    """Returns a tuple representing the node that can be understood by the PXP interpreter."""
    *assignments, ret_statement = self.statements
    return ("program",
            ret_statement.type,
            tuple(a.to_tuple() for a in assignments if a.is_used),
            ret_statement.to_tuple())


class Assignment(ASTNode):
  """An Assignment node."""
  def __init__(self, coords, assignee, assignment):
    """Construct an Assignment node."""
    super().__init__(coords)
    self.assignee = assignee
    self.assignment = assignment
    self.is_used = False

  @property
  def children(self):
    """The assignee and assignment value representing the Assignment node."""
    yield self.assignee
    yield self.assignment

  def to_tuple(self):
    """Returns a tuple representing the node that can be understood by the PXP interpreter."""
    return ("assign", self.assignee.value, self.assignment.to_tuple())


class ReturnStatement(ASTNode):
  """The ReturnStatement of the program."""
  def __init__(self, coords, expression, type):
    """Construct a ReturnStatement node."""
    super().__init__(coords)
    self.expression = expression
    self.type = type

  @property
  def children(self):
    """The expression to be evaluated for return."""
    yield self.expression

  def to_tuple(self):
    """Returns a tuple representing the node that can be understood by the PXP interpreter."""
    return ("return", self.expression.to_tuple())


class FunctionCall(ASTNode):
  """A node representing a function call."""
  def __init__(self, coords, name, args, function=None):
    """Construct a FunctionCall instance."""
    super().__init__(coords)
    self.name = name
    self.args = args
    self.function = function

  @property
  def children(self):
    """The name and args of the function call."""
    yield self.name
    yield from self.args

  @property
  def type(self):
    """The return type of the function call."""
    return self.function.return_type

  def to_tuple(self):
    """Returns a tuple representing the node that can be understood by the PXP interpreter."""
    return ("fn", self.function.signatures[0], tuple(a.to_tuple() for a in self.args), self.coords)


class Branch(ASTNode):
  def __init__(self, coords, options):
    super().__init__(coords)
    self.options = options

  @property
  def children(self):
    yield from self.options

  @property
  def type(self):
    return self.options[0].type

  def to_tuple(self):
    return ("branch", tuple(o.to_tuple() for o in self.options), self.coords)


class BranchOption(ASTNode):
  def __init__(self, coords, result, predicate=None):
    super().__init__(coords)
    self.result = result
    self.predicate = predicate

  @property
  def children(self):
    yield self.result
    if self.predicate:
      yield self.predicate

  @property
  def type(self):
    return self.result.type

  def to_tuple(self):
    return ("branch_option",
            self.result.to_tuple(),
            self.predicate.to_tuple() if self.predicate else None)


class Switch(ASTNode):
  def __init__(self, coords, subject, cases):
    super().__init__(coords)
    self.subject = subject
    self.cases = cases

  @property
  def children(self):
    yield self.subject
    yield from self.cases

  @property
  def type(self):
    return self.cases[0].type

  def to_tuple(self):
    return ("switch",
            self.subject.to_tuple(),
            tuple(c.to_tuple() for c in self.cases),
            self.coords)


class SwitchCase(ASTNode):
  def __init__(self, coords, result, comparison=None):
    super().__init__(coords)
    self.result = result
    self.comparison = comparison

  @property
  def children(self):
    yield self.result
    if self.comparison:
      yield self.comparison

  @property
  def type(self):
    return self.result.type

  def to_tuple(self):
    return ("switch_case",
            self.result.to_tuple(),
            self.comparison.to_tuple() if self.comparison else None)


class Number(ASTLeaf):
  """A literal numeric value node."""
  def __init__(self, value, coords=None):
    """Construct the Number instance."""
    super().__init__(Decimal(value), "Number", coords)

  @classmethod
  def from_parse_node(cls, parse_node, coords):
    """Construct a Number instance from a parse tree node."""
    return cls(parse_node.svalue, coords)


class Boolean(ASTLeaf):
  """A literal boolean value node."""
  def __init__(self, value, coords=None):
    """Construct the Boolean instance."""
    super().__init__(value, "Boolean", coords)

  @classmethod
  def from_parse_node(cls, parse_node, coords):
    """Construct a Boolean instance from a parse tree node."""
    return cls(parse_node.svalue == "true", coords)


class String(ASTLeaf):
  """A literal string value node."""
  def __init__(self, value, coords=None):
    """Construct the String instance."""
    super().__init__(value, "String", coords)

  @classmethod
  def from_parse_node(cls, parse_node, coords):
    """Construct a String instance from a parse tree node."""
    return cls(parse_node.svalue[1:-1], coords)


class Identifier(ASTLeaf):
  """An identifier node."""
  def __init__(self, value, type=None, coords=None):
    """Construct the Identifier instance."""
    super().__init__(value, type, coords)

  @classmethod
  def from_parse_node(cls, parse_node, coords):
    """Construct an Identifier instance from a parse tree node."""
    if parse_node.svalue.startswith("["):
      value = parse_node.svalue[1:-1]
    else:
      value = parse_node.svalue

    return cls(value, None, coords)


class Variable(Identifier):
  """A variable instance, which is a special type of identifier."""
  pass

  def to_tuple(self):
    """Returns a tuple representing the node that can be understood by the PXP interpreter."""
    return ("var", self.value, self.coords)


def is_value(obj):
  """Returns True if the object is either an ASTLeaf or a python object that is considered a raw
  value in PXP."""
  return isinstance(obj, (ASTLeaf, Decimal, str, bool))


def from_value(obj):
  """If obj is an ASTLeaf, returns the leaf. Otherwise either a Number, String or Boolean ASTLeaf
  is returned based on the Python type of the object.
  """
  if isinstance(obj, ASTLeaf):
    return obj
  elif isinstance(obj, Decimal):
    return Number(obj)
  elif isinstance(obj, str):
    return String(obj)
  elif isinstance(obj, bool):
    return Boolean(obj)
  else:
    raise Exception("Unhandled value conversion type: {0}".format(obj.__class__.__name__))
