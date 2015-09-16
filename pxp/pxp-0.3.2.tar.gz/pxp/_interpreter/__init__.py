"""This package contains classes and methods for executing compiled pxp code."""

from pxp.compiler import Compiler
from pxp.scope import ScopeStack, DictScope
from pxp.stdlib import global_scope
from .resolver import Resolver


class Interpreter(object):
  """The Interpreter class executes compiled pxp code."""
  def __init__(self, scope=None):
    """Initialize the Interpreter instance.

    If scope is present, it will be passed to the push method of the instance's ScopeStack.
    """
    self.scope = ScopeStack(global_scope)
    if scope:
      self.scope.push(scope)
    self.resolver = Resolver(self.scope)

  def interpret(self, source):
    """Compile and execute source code.

    source is pxp source text.
    """
    # Give the compiler all the non-global_scope scopes.
    compiler = Compiler(source, self.scope.scopes[1:])
    program = compiler.compile()
    return self.execute(program)

  @staticmethod
  def get_type(program):
    """Returns the return type of the return statement of the compiled program."""
    _, ptype, *_ = program
    return ptype

  def execute(self, program):
    """Execute compiled pxp instructions."""
    with self.scope.using(DictScope()):
      _, ptype, assignments, (_, return_exp) = program
      for assignment in assignments:
        self._assign(assignment)
      return self.resolver.resolve(return_exp)

  def _assign(self, assignment):
    """Handle an assignment instruction."""
    _, name, value = assignment
    self.scope.set_variable(name, value)
