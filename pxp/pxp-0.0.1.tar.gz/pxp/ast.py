from decimal import Decimal

from pyebnf.operator import OptreeNode


def pprint(node, depth=0, indent="    "):
  spacing = indent * depth

  if isinstance(node, ASTLeaf):
    print("{0}{1}".format(spacing, node))
  elif isinstance(node, OptreeNode):
    op = node.operator
    if op:
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
  def __init__(self, coords):
    self.coords = coords

  def to_tuple(self):
    raise NotImplementedError()


class ASTNode(ASTNodeBase):
  def __init__(self, coords=None):
    super().__init__(coords)

  @property
  def children(self):
    raise StopIteration()


class ASTLeaf(ASTNodeBase):
  def __init__(self, value, type, coords=None):
    super().__init__(coords)
    self.value = value
    self.type = type

  def __repr__(self):
    return "{0}({1})".format(self.__class__.__name__, self.value)

  def __str__(self):
    return repr(self)

  def to_tuple(self):
    return ("val", self.type, str(self.value))


class Program(ASTNode):
  def __init__(self, coords, statements):
    super().__init__(coords)
    self.statements = statements

  @property
  def children(self):
    yield from self.statements

  def to_tuple(self):
    *assignments, ret_statement = self.statements
    return ("program", ) + \
           tuple(a.to_tuple() for a in assignments if a.is_used) + \
           (ret_statement.to_tuple(), )


class Assignment(ASTNode):
  def __init__(self, coords, assignee, assignment):
    super().__init__(coords)
    self.assignee = assignee
    self.assignment = assignment
    self.is_used = False

  @property
  def children(self):
    yield self.assignee
    yield self.assignment

  def to_tuple(self):
    return ("assign", self.assignee.value, self.assignment.to_tuple())


class ReturnStatement(ASTNode):
  def __init__(self, coords, expression):
    super().__init__(coords)
    self.expression = expression

  @property
  def children(self):
    yield self.expression

  def to_tuple(self):
    return ("return", self.expression.to_tuple())


class FunctionCall(ASTNode):
  def __init__(self, coords, name, args, function=None):
    super().__init__(coords)
    self.name = name
    self.args = args
    self.function = function

  @property
  def children(self):
    yield self.name
    yield from self.args

  @property
  def type(self):
    return self.function.return_type

  def to_tuple(self):
    return ("fn", self.function.signatures[0]) + tuple(a.to_tuple() for a in self.args) + (self.coords, )


class Number(ASTLeaf):
  def __init__(self, value, coords=None):
    super().__init__(Decimal(value), "Number", coords)

  @classmethod
  def from_parse_node(cls, parse_node, coords):
    return cls(parse_node.svalue, coords)


class Boolean(ASTLeaf):
  def __init__(self, value, coords=None):
    super().__init__(value, "Boolean", coords)

  @classmethod
  def from_parse_node(cls, parse_node, coords):
    return cls(parse_node.svalue == "true", coords)


class String(ASTLeaf):
  def __init__(self, value, coords=None):
    super().__init__(value, "String", coords)

  @classmethod
  def from_parse_node(cls, parse_node, coords):
    return cls(parse_node.svalue[1:-1], coords)


class Identifier(ASTLeaf):
  def __init__(self, value, type=None, coords=None):
    super().__init__(value, type, coords)

  @classmethod
  def from_parse_node(cls, parse_node, coords):
    if parse_node.svalue.startswith("["):
      value = parse_node.svalue[1:-1]
    else:
      value = parse_node.svalue

    return cls(value, None, coords)


class Variable(Identifier):
  pass

  def to_tuple(self):
    return ("var", self.value, self.coords)


def is_value(obj):
  return isinstance(obj, (ASTLeaf, Decimal, str, bool))


def from_value(obj):
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
