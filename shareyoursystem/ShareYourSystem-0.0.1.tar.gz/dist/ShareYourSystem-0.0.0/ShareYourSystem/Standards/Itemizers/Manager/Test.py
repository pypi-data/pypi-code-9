#<ImportSpecificModules>
from ShareYourSystem.Standards.Classors.Representer import _print
from ShareYourSystem.Standards.Objects import Parenter
#</ImportSpecificModules>

#Print a version of the class
_print(dict(Parenter.ParenterClass.__dict__.items()))

#Print a version of this object
_print(Parenter.ParenterClass())

#Print a version of his __dict__
_print(Parenter.ParenterClass().__dict__)

#Test
_print(Parenter.attest_parent(),**{'RepresentingAlineaIsBool':False})