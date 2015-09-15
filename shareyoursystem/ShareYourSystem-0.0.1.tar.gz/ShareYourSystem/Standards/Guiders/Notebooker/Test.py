#<ImportSpecificModules>
from ShareYourSystem.Standards.Classors.Representer import _print
from ShareYourSystem.Standards.Objects import Loader
#</ImportSpecificModules>

#Print a version of the class
_print(dict(Loader.LoaderClass.__dict__.items()))

#Print a version of this object
_print(Loader.LoaderClass())

#Print a version of his __dict__
_print(Loader.LoaderClass().__dict__)
