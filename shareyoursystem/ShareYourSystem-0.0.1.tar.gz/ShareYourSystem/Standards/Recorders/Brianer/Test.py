#<ImportSpecificModules>
from ShareYourSystem.Standards.Classors.Representer import _print
from ShareYourSystem.Standards.Objects import Structurer
#</ImportSpecificModules>

#Print a version of the class
_print(dict(Structurer.StructurerClass.__dict__.items()))

#Print a version of this object
_print(Structurer.StructurerClass())

#Print a version of his __dict__
_print(Structurer.StructurerClass().__dict__)

#Test
_print(Structurer.attest_structure(),**{'RepresentingAlineaIsBool':False})