# ImportModules
from ShareYourSystem.Standards.Classors.Representer import _print
from ShareYourSystem.Standards.Objects import Debugger

#Print a version of the class
_print(dict(Debugger.DebuggerClass.__dict__.items()))

#Print a version of this object
_print(Debugger.DebuggerClass())

#Print a version of his __dict__
_print(Debugger.DebuggerClass().__dict__)


