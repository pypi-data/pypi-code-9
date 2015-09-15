#<ImportSpecificModules>
from ShareYourSystem.Standards.Classors.Representer import _print
from ShareYourSystem.Standards.Objects import Setter
#</ImportSpecificModules>

#Print a version of the class
_print(dict(Setter.SetterClass.__dict__.items()))

#Print a version of this object
_print(Setter.SetterClass())

#Print a version of his __dict__
_print(Setter.SetterClass().__dict__)

#Test
print(Setter.attest_set())