#ImportModules
from ShareYourSystem.Standards.Classors.Representer import _print
from ShareYourSystem.Standards.Objects import Inserter

#Print a version of the class
_print(dict(Inserter.InserterClass.__dict__.items()))

#Print a version of this object
_print(Inserter.InserterClass())

#Print a version of his __dict__
_print(Inserter.InserterClass().__dict__)

#Test
_print(Inserter.attest_insert())
