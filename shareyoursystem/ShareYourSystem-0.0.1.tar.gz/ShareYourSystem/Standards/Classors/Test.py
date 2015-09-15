#<ImportSpecificModules>
from ShareYourSystem.Standards.Classors.Representer import _print
from ShareYourSystem import Classors
#</ImportSpecificModules>

#Print a version of the class
_print(dict(Classors.ClassorsClass.__dict__.items()))

#Print a version of this object
_print(Classors.ClassorsClass())

#Print a version of his __dict__
_print(Classors.ClassorsClass().__dict__)

