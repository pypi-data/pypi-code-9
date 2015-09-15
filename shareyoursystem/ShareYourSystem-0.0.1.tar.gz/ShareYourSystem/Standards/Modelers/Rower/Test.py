#ImportModules
from ShareYourSystem.Standards.Classors.Representer import _print
from ShareYourSystem.Standards.Objects import Rower

#Print a version of the class
_print(dict(Rower.RowerClass.__dict__.items()))

#Print a version of this object
_print(Rower.RowerClass())

#Print a version of his __dict__
_print(Rower.RowerClass().__dict__)

#Test
_print(Rower.attest_row())
