#ImportModules
from ShareYourSystem.Standards.Classors.Representer import _print
from ShareYourSystem.Standards.Objects import Modeler

#Print a version of the class
_print(dict(Modeler.ModelerClass.__dict__.items()))

#Print a version of this object
_print(Modeler.ModelerClass())

#Print a version of his __dict__
_print(Modeler.ModelerClass().__dict__)

#Test
_print(Modeler.attest_model())