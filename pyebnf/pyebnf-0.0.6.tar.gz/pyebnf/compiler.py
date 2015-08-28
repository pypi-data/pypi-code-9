"""Contains methods for compiling an EBNF grammar parse tree into a Parser."""

import re
from collections import namedtuple, Counter

from .operator import Operator, OperatorNode, OptreeNode, infix_to_optree
from .parser import Parser, TokenType
from .util import esc_split


OP_ASSIGN = Operator("=", 1)
OP_ALTERNATE = Operator("|", 2)
OP_WS_CONCAT = Operator(".", 3)
OP_CONCAT = Operator(",", 4)
OP_EXCLUDE = Operator("-", 5)
OP_REP = Operator("*", 6)
OPERATORS = [
  OP_ASSIGN,
  OP_ALTERNATE,
  OP_CONCAT,
  OP_WS_CONCAT,
  OP_EXCLUDE,
  OP_REP ]
OPERATOR_IDX = {o.symbol: o for o in OPERATORS}
HANDLERS = {}


Identifier = namedtuple("Identifier", ["name"])
Terminal = namedtuple("Terminal", ["value"])
GroupingGroup = namedtuple("GroupingGroup", ["expression"])
RepetitionGroup = namedtuple("RepetitionGroup", ["expression", "lower_bound", "upper_bound"])
RepetitionGroup.__new__.__defaults__ = (None, None)
SpecialHandling = namedtuple("SpecialHandling", ["value"])
Rule = namedtuple("Rule", ["name", "definition"])
Directive = namedtuple("Directive", ["type", "args"])


def compile_source(source):
  """Returns the python source code for a parser defined by the ebnf parser."""
  content, directives, comments = split_source(source)
  grammar = Parser().parse(content)
  rules_source = _get_rules_source(content, grammar)
  return compile_grammar(grammar, directives=directives, rules_source=rules_source)


def split_source(source):
  """Splits the source code into comments, directives and content.

  A directive is any line that starts with '#!'.
  A comment is any other line that starts with '#'.
  Content is all other lines.

  The return value is a list of comments, a list of directives, and the content as a single block
  of text.
  """
  comments = []
  directives = []
  content = []
  for line in source.split("\n"):
    if line.startswith("#!"):
      directives.append(line[2:].strip())
    elif line.startswith("#"):
      comments.append(line[1:].strip())
    else:
      content.append(line)

  return ("\n".join(content), list(_parse_directives(directives)), comments)


def compile_grammar(grammar, *, directives=None, rules_source=None, indent="  "):
  """Given a grammar returned from a parser, return the python source code for the parser that the
  grammar represents.
  """
  rules = list(_grammar_to_rules(grammar))
  if rules_source is None:
    rules_source = {}

  duplicate_rules = [role_name for role_name, count in Counter(r.name for r in rules).items() if count > 1]
  if duplicate_rules:
    raise Exception("Duplicate rules found: {0}".format(", ".join(duplicate_rules)))

  rule_defs = [_compile_rule(rule, source=rules_source.get(rule.name), indent=indent) for rule in rules]
  return _heading(rules, directives, indent=indent) + "\n".join(rule_defs)


def _heading(rules, directives, *, indent="  "):
  """Returns the heading for the python parser source, including the imports and TokenType enum, and
  first lines of the Parser class definition.
  """
  rule_config_idx = {}
  parser_base = "ParserBase"
  entry_point = rules[0].name

  if directives is not None:
    rule_config_idx = {d.args["name"]: d for d in directives if d.type == "rule"}

    base_dir = _find_directive(directives, "base")
    if base_dir:
      parser_base = base_dir.args["value"]

    ep_dir = _find_directive(directives, "entry_point")
    if ep_dir:
      entry_point = ep_dir.args["value"]

  imports = """from enum import Enum

from pyebnf.parser_base import ParserBase, get_printable_character, get_whitespace_character
from pyebnf.primitive import Node, NodeType, alternation, concatenation
from pyebnf.primitive import exclusion, option, repetition, terminal

{imports}


""".format(imports="\n".join(d.args.get("value") for d in _find_directives(directives, "import")))

  token_types = ["{indent}{name} = {value}".format(indent=indent, name=r.name, value=i+ 1) for i, r in enumerate(rules)]
  tokens_def = """class TokenType(Enum):
{token_types}


""".format(token_types="\n".join(token_types))

  gen_proxy_defs = [_get_gen_proxy_def(rule, rule_config_idx.get(rule.name), indent=indent) for rule in rules]

  class_def = """class Parser({parser_base}):
{indent}def entry_point(self, text):
{indent}{indent}yield from self.{entry_point}(text)

{gen_proxies}
""".format(indent=indent,
           parser_base=parser_base,
           entry_point=_to_fxn_name(entry_point),
           gen_proxies="\n".join(gen_proxy_defs))

  return imports + tokens_def + class_def


def _parse_directives(directives):
  """Parses directives.

  A directive is a type name followed by 0 or more key=value pairs, delimited by a single space. If
  a key or value needs to have whitespace, escape the whitespace by placing a backslash directly
  ahead of it.
  """
  for directive in directives:
    dtype, *args = esc_split(directive, ignore_empty=True)
    yield Directive(dtype, {key: value for key, value in (esc_split(arg, "=") for arg in args)})


def _find_directive(directives, pred):
  """Returns the first directive that matches pred, or None if no directives match.

  pred is either a string which will be compared to the directive type, or a callable that accepts
  a directive as its only argument and returns True for directives that match.
  """
  if directives:
    for directive in directives:
      if _directive_matches(directive, pred):
        return directive
  return None


def _find_directives(directives, pred):
  """Generates directives that matches pred, or None if no directives match.

  pred is either a string which will be compared to the directive type, or a callable that accepts
  a directive as its only argument and returns True for directives that match.
  """
  if directives:
    for directive in directives:
      if _directive_matches(directive, pred):
        yield directive


def _directive_matches(directive, pred):
  """Returns true if the given directive matches the predicate.

  If pred is a string, it checks that directive.type == pred. Otherwise it treats pred like a
  callable and passes directive to it, returning the result.
  """
  if isinstance(pred, str):
    return directive.type == pred
  else:
    return pred(directive)


def _grammar_to_rules(grammar):
  """Generates rules from a grammar parse tree."""
  for rule in grammar.children:
    name, _, expression, _ = rule.children
    compiled_expression = _expression_to_optree(expression)
    yield Rule(name.svalue, compiled_expression)


def _get_rules_source(source, grammar):
  """Returns a dictionary of rule_name -> rule_source.

  source should be the preprocessed source from split_source.
  grammar is the parse tree
  """
  rule_list = list(grammar.children)
  rule_sources = {}
  source_len = len(source)

  for i in range(len(rule_list)):
    rule = rule_list[i]
    start_pos = source_len - rule.position
    if i + 1 < len(rule_list):
      end_pos = source_len - rule_list[i + 1].position
    else:
      end_pos = None
    rule_name = rule.children[0].svalue
    rule_sources[rule_name] = source[start_pos:end_pos].strip()
  return rule_sources


def _expression_to_optree(expression):
  """Converts an expression to an optree."""
  expression.flatten(lambda c, p: c.is_type(TokenType.expression) and c.is_type(p.node_type))
  tokens = []

  for child in expression.children:
    handler = HANDLERS.get(child.node_type)
    if handler is None:
      raise Exception("Unhandled node type: {0} :: {1}".format(child.node_type, child))
    else:
      tokens.extend(handler(child))

  optree = _remove_grouping_groups(infix_to_optree(tokens))
  return optree


def _remove_grouping_groups(optree):
  """Grouping groups are implied by optrees, this function hoists up grouping group expressions to
  the parent node.
  """
  new_operands = []
  for idx, operand in enumerate(optree.operands):
    if isinstance(operand, OptreeNode):
      new_operands.append(_remove_grouping_groups(operand))
    elif isinstance(operand, GroupingGroup):
      new_operands.append(operand.expression)
    else:
      new_operands.append(operand)
  return OptreeNode(optree.opnode, new_operands)


def _get_gen_proxy_def(rule, directive, *, indent):
  """Generated parsers have rule generation proxies. Each rule will defer to one for altering their
  generated tree, allowing you to iterate_merge and iterate_reduce in one section of the source.

  Parser directives can handle most cases of this and touching the code shouldn't be necessary.
  """
  config = directive.args if directive else None
  if config is None:
    gen = "yield from gen(text)"
  else:
    token_type = config.get("token_type", rule.name)
    imode = config.get("imode", "merge")

    if imode == "merge":
      meth = "Node.iterate_merge"
      gen_fmt = "yield from {meth}(TokenType.{token_type}, gen, text)"
    elif imode == "reduce":
      meth = "Node.iterate_reduce"
      gen_fmt = "yield from {meth}(TokenType.{token_type}, gen, text)"
    else:
      raise CompilerError("Unknown imode: {0}".format(imode))

    gen = gen_fmt.format(meth=meth,
                         token_type=token_type)
  return """{indent}def _gen{rule_fxn_name}(self, gen, text):
{indent}{indent}{gen}
""".format(indent=indent,
           rule_fxn_name=_to_fxn_name(rule.name),
           gen=gen)


def _compile_rule(rule, *, source, indent):
  """Turns a rule into the python source text that it represents."""
  head, *body = _node_to_code(rule.definition, depth=2, indent=indent)
  lines = [head.strip()] + body
  return """{indent}def {rule_fxn_name}(self, text):
{indent}{indent}\"\"\"{source}\"\"\"
{indent}{indent}self.attempting(text)
{indent}{indent}gen = {generator}
{indent}{indent}yield from self._gen{rule_fxn_name}(gen, text)
""".format(indent=indent,
           rule_fxn_name=_to_fxn_name(rule.name),
           source=_indent_rule_source_lines(source, indent * 2 + "   "),
           generator="\n".join(lines))


def _node_to_code(node, depth, indent):
  """A switching method that delegates to other methods based on the type of the node."""
  if isinstance(node, OptreeNode):
    return _opnode_to_code(node, depth, indent)
  else:
    return _operand_to_code(node, depth, indent)


def _opnode_to_code(optree, depth, indent):
  """A switching method that delegates to other methods based on the operator of the optree."""
  opnode = optree.opnode
  if opnode is None:
    return _operand_to_code(optree.operands[0], depth, indent)
  elif opnode.operator is OP_ALTERNATE:
    return _alternate_op_to_code(optree, depth, indent)
  elif opnode.operator is OP_CONCAT:
    return _concat_op_to_code(optree, depth, indent)
  elif opnode.operator is OP_WS_CONCAT:
    return _concat_op_to_code(optree, depth, indent, False)
  elif opnode.operator is OP_EXCLUDE:
    return _exclude_op_to_code(optree, depth, indent)
  elif opnode.operator is OP_REP:
    return _rep_op_to_code(optree, depth, indent)
  else:
    raise Exception("Unhandled operator: {0}".format(opnode.operator.symbol))


def _operand_to_code(operand, depth, indent):
  """A switching method that delegates to other methods based on the node type."""
  if isinstance(operand, Identifier):
    return _identifier_to_code(operand, depth, indent)
  elif isinstance(operand, Terminal):
    return _terminal_to_code(operand, depth, indent)
  elif isinstance(operand, RepetitionGroup):
    return _repetition_group_to_code(operand, depth, indent)
  elif isinstance(operand, SpecialHandling):
    return _special_handling_to_code(operand, depth, indent)
  else:
    raise Exception("Unhandled operand type {0}".format(operand.__class__.__name__))


def _hoist(operands, predicate):
  """Flattens a list of optree operands based on a predicate."""
  hopper = list(operands)
  new_operands = []
  while hopper:
    target = hopper.pop(0)
    if predicate(target):
      hopper = list(target.operands) + hopper
    else:
      new_operands.append(target)
  return new_operands


def _concat_op_to_code(opnode, depth, indent, ignore_ws=True):
  """Generates the python source that represents a concat operation."""
  spacing = depth * indent

  # We'll only hoist similar concats.
  hoist_target = OP_CONCAT if ignore_ws else OP_WS_CONCAT
  operands = _hoist(opnode.operands, lambda t: isinstance(t, OptreeNode) and t.opnode.operator is hoist_target)

  lines = [spacing + "concatenation(["]
  for i, operand in enumerate(operands):
    lines.extend(_node_to_code(operand, depth + 1, indent))
    if i < len(operands) - 1:
      lines[-1] += ","

  if ignore_ws:
    lines.append(spacing + "], True)")
  else:
    lines.append(spacing + "], False)")

  return lines


def _alternate_op_to_code(opnode, depth, indent):
  """Generates the python source that represents an alternate operation."""
  spacing = depth * indent
  operands = _hoist(opnode.operands,
                    lambda t: isinstance(t, OptreeNode) and t.opnode.operator is OP_ALTERNATE)

  lines = [spacing + "alternation(["]
  for i, operand in enumerate(operands):
    lines.extend(_node_to_code(operand, depth + 1, indent))
    if i < len(operands) - 1:
      lines[-1] += ","
  lines.append(spacing + "])")
  return lines


def _exclude_op_to_code(opnode, depth, indent):
  """Generates the python source that represents an exclude operation."""
  spacing = depth * indent
  lines = [spacing + "exclusion("]
  for i, operand in enumerate(opnode.operands):
    lines.extend(_node_to_code(operand, depth + 1, indent))
    if i < len(opnode.operands) - 1:
      lines[-1] += ","
  lines.append(spacing + ")")
  return lines


def _repetition_group_to_code(rep_group, depth, indent):
  """Generates the python source the represents a repetition operation."""
  spacing = depth * indent

  if (rep_group.lower_bound is None and rep_group.upper_bound is None) or \
     (rep_group.lower_bound == rep_group.upper_bound):
    lines = [spacing + "repetition("]
    lines.extend(_node_to_code(rep_group.expression, depth + 1, indent))
    lines[-1] += ","
    lines.append("{0}{1}bound={2}".format(spacing, indent, rep_group.lower_bound or -1))
    lines.append(spacing + ")")

  elif rep_group.lower_bound is None and rep_group.upper_bound == 1:
    lines = [spacing + "option("]
    lines.extend(_node_to_code(rep_group.expression, depth + 1, indent))
    lines.append(spacing + ")")

  else:
    raise CompilerError("Invalid bound pairing: [{0}, {1}]".format(rep_group.lower_bound,
                                                                   rep_group.upper_bound))

  return lines


def _identifier_to_code(identifier, depth, indent):
  """Generates the python source for one rule definition to call another."""
  spacing = depth * indent
  return ["{0}self.{1}".format(spacing, _to_fxn_name(identifier.name))]


_term_reps = (("\\", "\\\\"),
              ("\\\\n", "\\n"))

def _terminal_to_code(terminal, depth, indent):
  """Generates the python source the terminal represents."""
  spacing = depth * indent
  v = terminal.value
  for s, t in _term_reps:
    v = v.replace(s, t)
  return ["{0}terminal({1})".format(spacing, v)]


def _special_handling_to_code(special_handling, depth, indent):
  """Generates the code for a special handling rule."""
  spacing = depth * indent
  if special_handling.value == "all_printable_characters":
    return ["{0}get_printable_character".format(spacing)]
  elif special_handling.value == "all_whitespace_characters":
    return ["{0}get_whitespace_character".format(spacing)]
  else:
    return ["""{0}self.special_handling_default("{1}")""".format(spacing, special_handling.value)]


def _handle_node(*node_types):
  """A decorator for designating node handlers by name. Each handler should return a list of nodes
  that will replace them in the tree.
  """
  def wrapper(fx):
    """The actual wrapper function."""
    for node_type in node_types:
      HANDLERS[node_type] = fx
    return fx
  return wrapper


def _ignore_node(node):
  """Ignores a node by returning an empty list for its replacement."""
  return []


@_handle_node(TokenType.operator)
def _handle_operator(node):
  """Returns an OperatorNode instance."""
  return [OperatorNode(OPERATOR_IDX[node.svalue], node.position)]


@_handle_node(TokenType.identifier)
def _handle_identifier(node):
  """Returns an Identifier instance."""
  return [Identifier(node.svalue)]


@_handle_node(TokenType.terminal)
def _handle_terminal(node):
  """Returns a Terminal instance."""
  return [Terminal(node.svalue)]


@_handle_node(TokenType.grouping_group)
def _handle_grouping_group(node):
  """Returns a GroupingGroup instance."""
  _, expression, _ = node.children
  comp_expr = _expression_to_optree(expression)
  return [GroupingGroup(comp_expr)]


@_handle_node(TokenType.repetition_group)
def _handle_repetition_group(node):
  """Returns an unbounded RepetitionGroup instance."""
  _, expression, _ = node.children
  comp_expr = _expression_to_optree(expression)
  return [RepetitionGroup(comp_expr)]


@_handle_node(TokenType.option_group)
def _handle_option_group(node):
  """Returns a RepetitionGroup instance with a limit of 1."""
  _, expression, _ = node.children
  comp_expr = _expression_to_optree(expression)
  return [RepetitionGroup(comp_expr, None, 1)]


@_handle_node(TokenType.special_handling)
def _handle_special_handling(node):
  """Returns a SpecialHandling instance."""
  _, value, _ = node.children
  return [SpecialHandling(value.svalue)]


def _to_fxn_name(name):
  """Converts a name into a parser function name."""
  new_name = re.sub(r"(\W|_)+", "_", name.strip())
  return "_" + new_name


def _to_special_handling_name(name):
  """Converts a name into a parser special handling name."""
  return _to_fxn_name("sh_" + name)


def _indent_rule_source_lines(text, indent):
  """Indents rule source code for including as doc strings. The first line is not indented because
  it is inline with the opening quotes.
  """
  first, *lines = text.split("\n")
  ilines = [indent + line for line in lines]
  return "\n".join([first] + ilines)


if __name__ == "__main__":
  import sys
  if len(sys.argv) > 1:
    for filename in sys.argv[1:]:
      with open(filename, "r") as rf:
        print(compile_source(rf.read()))
  else:
    print(compile_source(sys.stdin))
