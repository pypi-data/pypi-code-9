#<ImportSpecificModules>
from ShareYourSystem.Standards.Classors.Representer import _print
from ShareYourSystem.Standards.Objects import Hdformater
#</ImportSpecificModules>

#Print a version of the class
_print(dict(Hdformater.HdformaterClass.__dict__.items()))

#Print a version of this object
_print(Hdformater.HdformaterClass())

#Print a version of his __dict__
_print(Hdformater.HdformaterClass().__dict__)

#Test
_print(Hdformater.attest_hdformat(),**{'RepresentingAlineaIsBool':False})