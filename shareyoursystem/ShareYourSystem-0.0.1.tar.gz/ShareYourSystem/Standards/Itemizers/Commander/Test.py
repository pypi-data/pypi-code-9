#<ImportSpecificModules>
from ShareYourSystem.Standards.Classors.Representer import _print
from ShareYourSystem.Standards.Objects import Commander
#</ImportSpecificModules>

#Print a version of the class
_print(dict(Commander.CommanderClass.__dict__.items()))

#Print a version of this object
_print(Commander.CommanderClass())

#Print a version of his __dict__
_print(Commander.CommanderClass().__dict__)

#Test
_print(Commander.attest_commandAllSetsForEach(),**{'RepresentingAlineaIsBool':False})
_print(Commander.attest_commandEachSetForAll(),**{'RepresentingAlineaIsBool':False})