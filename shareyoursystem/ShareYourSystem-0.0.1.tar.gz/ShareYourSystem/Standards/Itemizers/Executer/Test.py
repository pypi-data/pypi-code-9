#<ImportSpecificModules>
from ShareYourSystem.Standards.Classors.Representer import _print
from ShareYourSystem.Standards.Objects import Executer
#</ImportSpecificModules>

#Print a version of the class
_print(dict(Executer.ExecuterClass.__dict__.items()))

#Print a version of this object
_print(Executer.ExecuterClass())

#Print a version of his __dict__
_print(Executer.ExecuterClass().__dict__)

#Test
_print(Executer.attest_execute(),**{'RepresentingAlineaIsBool':False})