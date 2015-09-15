#ImportModules
from ShareYourSystem.Standards.Classors.Representer import _print
from ShareYourSystem.Standards.Objects import Retriever

#Print a version of the class
_print(dict(Retriever.RetrieverClass.__dict__.items()))

#Print a version of this object
_print(Retriever.RetrieverClass())

#Print a version of his __dict__
_print(Retriever.RetrieverClass().__dict__)

#Test
print(Retriever.attest_retrieve())
