#/######################/#
# Import
#

#ImportModules
import ShareYourSystem as SYS

#/######################/#
# Define you hierarchic objects
#

#addDo
SYS.Doer.addDo('Oscillater','Oscillate','Oscillating','Oscillated')

#Define a Moduler class
@SYS.ClasserClass(**{
	'ClassingStructureVariable':[
		('Mode','Modes'),
		('Resonance','Resonances')
	]
})
class OscillaterClass(SYS.StructurerClass):
								
	def default_init(self,
						**_KwargVariablesDict
					):

		#Call the parent init method
		SYS.StructurerClass.__init__(self,**_KwargVariablesDict)

#addDo
SYS.Doer.addDo('Networker','Network','Networking','Networked')

#Define a Moduler class
@SYS.ClasserClass(**{
	'ClassingStructureVariable':[
		('Population','Populations'),
		('Neuron','Neurons')
	]
})
class NetworkerClass(OscillaterClass):
								
	def default_init(self,
						**_KwargVariablesDict
					):

		#Call the parent init method
		OscillaterClass.__init__(self,**_KwargVariablesDict)
	
#/######################/#
# Define one instance
#

#set
MyNetworker = NetworkerClass()

#/######################/#
# Print
#

#print
print('MyNetworker is ')
SYS._print(MyNetworker.StructuresOrderedDict)

