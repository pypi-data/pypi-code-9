from pxp.compiler import Compiler
from pxp.scope import ScopeStack, DictScope
from pxp.stdlib import global_scope
from .resolver import Resolver


class Interpreter(object):
  def __init__(self, scope=None):
    self.scope = ScopeStack(global_scope)
    if scope:
      self.scope.push(scope)
    self.resolver = Resolver(self.scope)

  def interpret(self, source):
    compiler = Compiler(source)
    return self.execute(compiler.compile())

  def execute(self, program):
    with self.scope.using(DictScope()):
      _, *assignments, (_, return_exp) = program
      for assignment in assignments:
        self._assign(assignment)
      return self.resolver.resolve(return_exp)

  def _assign(self, assignment):
    _, name, value = assignment
    self.scope.set_variable(name, value)
