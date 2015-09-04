"""PXP: Python eXPression languate

PXP is a simple, python hosted expression language, intended to be used to calculate expressions
in code in a safe environment.
"""

from .compiler import Compiler
from .interpreter import Interpreter
from . import scope
