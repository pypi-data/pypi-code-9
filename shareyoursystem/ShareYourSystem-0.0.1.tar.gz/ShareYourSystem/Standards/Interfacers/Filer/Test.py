#<ImportSpecificModules>
from ShareYourSystem.Standards.Classors.Representer import _print
from ShareYourSystem.Standards.Objects import Filer
#</ImportSpecificModules>

#Print a version of the class
_print(dict(Filer.FilerClass.__dict__.items()))

#Print a version of this object
_print(Filer.FilerClass())

#Print a version of his __dict__
_print(Filer.FilerClass().__dict__)
