#ImportSpecificModules>
from ShareYourSystem.Standards.Classors.Representer import _print
from ShareYourSystem.Standards.Objects import Noder

#Print a version of the class
_print(dict(Noder.NoderClass.__dict__.items()))

#Print a version of this object
_print(Noder.NoderClass())

#Print a version of his __dict__
_print(Noder.NoderClass().__dict__)

#Test
print(Noder.attest_node())