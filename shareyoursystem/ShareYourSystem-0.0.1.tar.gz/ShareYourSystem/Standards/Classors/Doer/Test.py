#<ImportSpecificModules>
#from ShareYourSystem.Standards.Classors.Representer import _print
import json
from ShareYourSystem.Standards.Classors import Doer
from ShareYourSystem.Standards.Objects import Initiator
#</ImportSpecificModules>

#Print some special attributes of the class
print('Doer.DoerClass.DefaultAttributeItemTuplesList is')
print(Doer.DoerClass.DefaultAttributeItemTuplesList)

#Print a version of this object
print(Doer.DoerClass())

#Print a version of his __dict__
print(Doer.DoerClass().__dict__)

@Doer.DoerClass()
class MakerClass(Initiator.InitiatorClass):

	def default_init(self,
						Int,
						_MakingInt=0,
						_MadeFloat=1.,
						_MadeStr=""
				):
		pass

	def make():
		pass

#Print some special attributes from the class
print(MakerClass.DoerStr)
print(MakerClass.DoStr)
print(MakerClass.DoneStr)
print(MakerClass.DoingStr)
print(MakerClass.DoingAttributeVariablesOrderedDict)
print(MakerClass.DoneAttributeVariablesOrderedDict)
print(MakerClass.MakingInt)

