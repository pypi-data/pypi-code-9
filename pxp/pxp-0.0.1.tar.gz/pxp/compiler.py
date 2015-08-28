import string

from pyebnf.exception import ParserError
from pyebnf.operator import OperatorNode, OptreeNode, infix_to_optree
from pyebnf.primitive import NodeType

import pxp.util as util
from .ast import Assignment, Boolean, FunctionCall, Identifier, Number, Program, ReturnStatement
from .ast import String, Variable, is_value, from_value
from .exception import CompilerError, ScopeError
from .operator import operator_index
from .parser import Parser, TokenType
from .scope import DictScope, ScopeStack
from .stdlib import global_scope
from .stdlib.types import type_defaults


HANDLERS = {}


def _prepare_source(source, eof_marker="\\eof"):
  source = source.rstrip(string.whitespace)
  if not source.endswith(eof_marker):
    return source + "\n{0}".format(eof_marker)
  return source

class Compiler(object):
  version = (0, 0, 1)

  def __init__(self, source):
    self.source = _prepare_source(source)
    self.source_len = len(source)
    self.scope = ScopeStack(global_scope)
    self._source_newlines = None
    self._parse_tree = None
    self._abstract_syntax_tree = None
    self._externs = DictScope()
    self._resolving_variables = []

    self.scope.push(self._externs)

  def compile(self):
    return self.abstract_syntax_tree.to_tuple()

  @property
  def parse_tree(self):
    if self._parse_tree is None:
      try:
        self._parse_tree = Parser().parse(self.source)
      except ParserError as pe:
        raise self._get_compiler_error(pe.position, pe.message)
      self._parse_tree.trim(_trim_predicate)
      self._parse_tree.flatten(_flatten_predicate)
    return self._parse_tree

  @property
  def abstract_syntax_tree(self):
    if self._abstract_syntax_tree is None:
      self._abstract_syntax_tree = self._generate_ast(self.parse_tree)[0]
    return self._abstract_syntax_tree

  @property
  def source_newlines(self):
    if self._source_newlines is None:
      self._source_newlines = util.get_newline_positions(self.source)
    return self._source_newlines

  def _get_node_coords(self, node):
    return self._get_coords(self.source_len - node.position)

  def _get_coords(self, pos):
    return util.get_line_and_char(self.source_newlines, pos)

  def _get_compiler_error(self, pos, message):
    if isinstance(pos, int):
      coords = self._get_coords(pos)
    elif isinstance(pos, tuple):
      coords = pos
    else:
      coords = self._get_node_coords(pos)
    return CompilerError(coords, message)

  def _generate_ast(self, node):
    if not node.is_value:
      new_children = []
      for child in node.children:
        new_children.extend(self._generate_ast(child))
      return self._handle_container_node(node, new_children)
    else:
      return self._handle_value_node(node)

  def _ignore_node(self):
    return []

  def _handle_container_node(self, node, new_children):
    if node.is_type(TokenType.program):
      return self._handle_program(node, new_children)
    elif node.is_type(TokenType.assignment):
      return self._handle_assignment(node, new_children)
    elif node.is_type(TokenType.expression):
      return self._handle_expression(node, new_children)
    elif node.is_type(TokenType.subexpression):
      return self._handle_subexpression(node, new_children)
    elif node.is_type(TokenType.function_call):
      return self._handle_function_call(node, new_children)
    elif node.is_type(TokenType.return_statement):
      return self._handle_return_statement(node, new_children)
    else:
      raise Exception("Unhandled node type {0}".format(node.node_type))

  def _handle_value_node(self, node):
    if node.is_type(TokenType.comment):
      return self._ignore_node()
    elif node.is_type(TokenType.variable):
      return self._handle_variable(node)
    elif node.is_type(TokenType.string):
      return self._handle_string(node)
    elif node.is_type(TokenType.number):
      return self._handle_number(node)
    elif node.is_type(TokenType.operator):
      return self._handle_operator(node)
    elif node.is_type(TokenType.function_name):
      return self._handle_function_name(node)
    elif node.is_type(TokenType.directive):
      return self._handle_directive(node)
    else:
      raise Exception("Unhandled node type {0}".format(node.node_type))

  def _handle_program(self, node, new_children):
    return [Program(node, new_children)]

  def _handle_assignment(self, node, new_children):
    assignee, assignment = new_children
    anode = Assignment(node, assignee, assignment)
    self.scope.set_variable(assignee.value, assignment)
    self.scope.set_variable(assignee.value + ".__assign__", anode)
    return [anode]

  def _handle_variable(self, node):
    if node.svalue in ("true", "false"):
      return [Boolean.from_parse_node(node, self._get_node_coords(node))]
    else:
      return [Variable.from_parse_node(node, self._get_node_coords(node))]

  def _handle_string(self, node):
    return [String.from_parse_node(node, self._get_node_coords(node))]

  def _handle_number(self, node):
    return [Number.from_parse_node(node, self._get_node_coords(node))]

  def _handle_operator(self, node):
    return [OperatorNode(operator_index[node.svalue], self._get_node_coords(node))]

  def _handle_expression(self, node, new_children):
    return [infix_to_optree(new_children)]

  def _handle_subexpression(self, node, new_children):
    return new_children

  def _handle_function_name(self, node):
    return [Identifier.from_parse_node(node, self._get_node_coords(node))]

  def _handle_function_call(self, node, new_children):
    name, *args = new_children
    return [FunctionCall(node, name, args)]

  def _handle_return_statement(self, node, new_children):
    return [ReturnStatement(node, self._resolve_optree(new_children[0])[1])]

  def _handle_directive(self, node):
    command, *args = node.value.split()
    if command == "#extern":
      if len(args) == 2:
        etype, ename = args
        if etype not in type_defaults:
          raise self._get_compiler_error(node, "Unknown type {0} for {1} directive".format(etype, command))
        else:
          self._externs.set_variable(ename, type_defaults[etype])
      else:
        raise self._get_compiler_error(node, "Directive {0} expects exactly 2 arguments".format(command))
    else:
      raise self._get_compiler_error(node, "Unknown directive: {0}".format(command))
    return []

  def _resolve(self, obj):
    if isinstance(obj, OptreeNode):
      return self._resolve_optree(obj)
    elif isinstance(obj, Variable):
      return self._resolve_variable(obj)
    elif isinstance(obj, FunctionCall):
      return self._resolve_function_call(obj)
    elif is_value(obj):
      astn = from_value(obj)
      return (astn.type, astn)
    else:
      raise Exception("Unhandled type {0}".format(obj.__class__.__name__))

  def _resolve_optree(self, optree):
    new_operands = []
    types = []

    for operand in optree.operands:
      otype, newop = self._resolve(operand)
      new_operands.append(newop)
      types.append(otype)

    # operator is None -> Identity
    opnode = optree.opnode
    if opnode is None:
      return (types[0], new_operands[0])
    else:
      op_fn_name = "operator{0}".format(opnode.operator.symbol)
      fn_sig = (op_fn_name, ) + tuple(types)
      try:
        fn = self.scope.get_function(fn_sig)
      except ScopeError as ex:
        raise self._get_compiler_error(opnode.position, str(ex))
      return (fn.return_type, FunctionCall(opnode.position, Identifier(op_fn_name), new_operands, fn))

  def _resolve_variable(self, variable):
    name = variable.value
    if name in self._resolving_variables:
      raise self._get_compiler_error(variable.coords, "Circular reference: {0} -> {1}".format(" -> ".join(self._resolving_variables), name))

    try:
      value = self.scope.get_variable(name)
    except ScopeError as ex:
      raise self._get_compiler_error(variable.coords, str(ex))

    self._resolving_variables.append(name)

    if variable.type is None:
      otype, newop = self._resolve(value)
      variable.type = otype

      if not self.scope.is_constant(name):
        self.scope.overwrite_variable(name, newop)

        assign_var_name= "{0}.__assign__".format(name)
        if self.scope.contains_variable(assign_var_name):
          assn_node = self.scope.get_variable(assign_var_name)
          assn_node.assignment = newop
          assn_node.is_used = True

    self._resolving_variables.pop()

    return (variable.type, variable)

  def _resolve_function_call(self, function_call):
    if function_call.function is None:
      types, new_args = zip(*[self._resolve(arg) for arg in function_call.args])
      fn_sig = (function_call.name.value, ) + tuple(types)
      try:
        fn = self.scope.get_function(fn_sig)
      except ScopeError as ex:
        raise self._get_compiler_error(function_call.name.coords, str(ex))
      function_call.args = new_args
      function_call.function = fn

    return (function_call.function.return_type, function_call)


def _flatten_predicate(c, p):
  if c.is_type(TokenType.expression) and p.node_type == c.node_type:
    return True
  if c.is_type(TokenType.function_args) and p.is_type({TokenType.function_args, TokenType.function_call}):
    return True
  if isinstance(c.node_type, NodeType) and not c.is_type(NodeType.terminal):
    return True
  return False


def _trim_predicate(c):
  return c.is_type(NodeType.terminal)
