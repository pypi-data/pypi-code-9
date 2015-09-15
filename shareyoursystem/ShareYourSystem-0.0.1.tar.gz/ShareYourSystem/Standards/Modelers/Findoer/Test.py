#ImportModules
from ShareYourSystem.Standards.Classors.Representer import _print
from ShareYourSystem.Standards.Objects import Findoer

#Print a version of the class
_print(dict(Findoer.FindoerClass.__dict__.items()))

#Print a version of this object
_print(Findoer.FindoerClass())

#Print a version of his __dict__
_print(Findoer.FindoerClass().__dict__)

#Test
print(Findoer.attest_find())
