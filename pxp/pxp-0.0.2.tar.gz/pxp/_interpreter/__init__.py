"""This package contains classes and methods for executing compiled pxp code."""

from pxp.compiler import Compiler
from pxp.scope import ScopeStack, DictScope
from pxp.stdlib import global_scope
from .resolver import Resolver


class Interpreter(object):
  """The Interpreter class executes compiled pxp code."""
  def __init__(self, scope=None):
    """Initialize the Interpreter instance.

    scope is a pxp.scope.ScopeBase instance that will be pushed on top of the interpreter's
    ScopeStack. Each interpreter instance includes the stdlib.global_scope by default.
    """
    self.scope = ScopeStack(global_scope)
    if scope:
      self.scope.push(scope)
    self.resolver = Resolver(self.scope)

  def interpret(self, source):
    """Compile and execute source code.

    source is pxp source text.
    """
    compiler = Compiler(source)
    return self.execute(compiler.compile())

  def execute(self, program):
    """Execute compiled pxp instructions."""
    with self.scope.using(DictScope()):
      _, *assignments, (_, return_exp) = program
      for assignment in assignments:
        self._assign(assignment)
      return self.resolver.resolve(return_exp)

  def _assign(self, assignment):
    """Handle an assignment instruction."""
    _, name, value = assignment
    self.scope.set_variable(name, value)
