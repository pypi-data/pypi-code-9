#ImportModules
#from ShareYourSystem.Standards.Classors.Representer import _print
from ShareYourSystem.Standards.Classors import Propertiser
from ShareYourSystem.Standards.Objects import Initiator

#Print a version of the class
print(dict(Propertiser.PropertiserClass.__dict__.items()))

#Print a version of this object
print(Propertiser.PropertiserClass())

#Print a version of his __dict__
print(Propertiser.PropertiserClass().__dict__)

@Propertiser.PropertiserClass()
class MakerClass(Initiator.InitiatorClass):

	def default_init(self,
						Int,
						_MakingFloat={
										'DefaultValueType':property,
										'PropertyInitVariable':3.,
										'PropertyDocStr':"This is the making float"
										},
						_MakingList=[],
						_MadeInt=0	
				):
		
		#Definition an attribute
		self.MakeStr="I am a Maker with "+str(self.MakingFloat)

	#Definition a binding function
	def setMakingFloat(self,_SettingValueVariable):

		#Print
		print('I am going to make the job directly without make !')

		#set the value
		self._MakingFloat=_SettingValueVariable

		#Bind with MadeInt setting
		self.MadeInt=int(self._MakingFloat)

#Print some special attributes of the class
print('')
print('MakerClass.KeyStrsList is')
print(MakerClass.KeyStrsList)
print('MakerClass.InitInspectDict is')
print(MakerClass.InitInspectDict)
print('MakerClass.DefaultAttributeItemTuplesList is')
print(MakerClass.DefaultAttributeItemTuplesList)
print('MakerClass.MakinFloat is')
print(MakerClass.MakingFloat)

#Init an instance that is completely defined by its default __class__ attributes
print('')
print('Default instance')
MyMaker=MakerClass(3)

#
print(MyMaker)

#
print(MyMaker.__dict__)

#But
print(MyMaker.MakingFloat)
print(MyMaker.MakingList)
print(MyMaker.MadeInt)


#
print('')
print('Instance with a specific attribute')
MyMaker=MakerClass(3,_MakingFloat=5.)

#
print(MyMaker.__dict__)

#But
print(MyMaker.MakingFloat)
print(MyMaker.MakingList)
print(MyMaker.MadeInt)


#
print('')
print('Instance with specific attributes from kwarg also ')
MyMaker=MakerClass(3,_MakingFloat=5.,**{'MakingList':["hello"]})

#
print(MyMaker.__dict__)

#But
print(MyMaker.MakingFloat)
print(MyMaker.MakingList)
print(MyMaker.MadeInt)

#
print('')
print('Build Instances sharing attributes ')
MyFirstMaker=MakerClass(3)
MySecondMaker=MakerClass(3)
MakerClass.MakingFloat=4
print(MyFirstMaker.MakingFloat)
print(MySecondMaker.MakingFloat)

#Independent new settings
print('')
print('MyFirstMaker new independent settings')
MyFirstMaker.MakingFloat=5
MyFirstMaker.MakingList=['hello']
print(MyFirstMaker.__dict__)

print('')
print('At the scale of the class ')
print(MakerClass.MakingFloat)
print(MakerClass.MakingList)

print('')
print('For the second instance')
print(MySecondMaker.MakingFloat)
print(MySecondMaker.MakingList)

