#ImportSpecificModules>
from ShareYourSystem.Standards.Classors.Representer import _print
from ShareYourSystem.Standards.Objects import Folderer

#Print a version of the class
_print(dict(Folderer.FoldererClass.__dict__.items()))

#Print a version of this object
_print(Folderer.FoldererClass())

#Print a version of his __dict__
_print(Folderer.FoldererClass().__dict__)
