#ImportModules
import ShareYourSystem as SYS

#Define
@SYS.DoerClass()
class MakerClass(SYS.PrinterClass):

	def default_init(self,
						_MakingMyFloat=0.,  
						_MadeMyInt=0
					):
		SYS.PrinterClass.__init__(self)
	
#Definition a simple instance
SimpleMaker=MakerClass(_MakingMyFloat=2.)

#print
print('SimpleMaker is '+SYS._str(SimpleMaker))
print('')

#Represent a structured instance
ParentMaker=MakerClass()
ParentMaker.FirstChildMaker=MakerClass()
ParentMaker.CircularChildMaker=MakerClass()
ParentMaker.CircularChildMaker.ParentMaker=ParentMaker
ParentMaker.CircularChildMaker.SelfMaker=ParentMaker.CircularChildMaker

#print
print('ParentMaker is '+SYS._str(ParentMaker))
print('')

#Definition a derived class from the MakerClass
@SYS.DoerClass()
class BuilderClass(MakerClass):

	RepresentingKeyStrsList=['BuiltMyStr']

	def default_init(self,
						_BuildingMyStr='hello',  
						_BuiltMyStr='None'
					):
		MakerClass.__init__(self)

#Definition a simple instance
SimpleBuilder=BuilderClass(_MakingMyFloat=2.)

#print
print('SimpleBuilder is '+SYS._str(SimpleBuilder)) 

