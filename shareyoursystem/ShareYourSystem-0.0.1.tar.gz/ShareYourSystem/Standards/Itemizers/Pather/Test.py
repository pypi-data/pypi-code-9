#<ImportSpecificModules>
from ShareYourSystem.Standards.Classors.Representer import _print
from ShareYourSystem.Standards.Objects import Pather
#</ImportSpecificModules>

#Print a version of the class
_print(dict(Pather.PatherClass.__dict__.items()))

#Print a version of this object
_print(Pather.PatherClass())

#Print a version of his __dict__
_print(Pather.PatherClass().__dict__)

#Test
print(Pather.attest_path())