#/######################/#
# Import
#

#ImportModules
import ShareYourSystem as SYS

#/######################/#
# Define you hierarchic objects
#

#addDo
SYS.Doer.addDo('Recorder','Record','Recording','Recorded')

#Define a Moduler class
@SYS.ClasserClass(**{
	'ClassingStructureVariable':[
		('Trace','Traces'),
		('Sample','Samples')
	]
})
class RecorderClass(SYS.StructurerClass):
								
	def default_init(self,
						**_KwargVariablesDict
					):

		#Call the parent init method
		SYS.StructurerClass.__init__(self,**_KwargVariablesDict)
	
#/######################/#
# Define one instance
#

MyRecorder=RecorderClass(
	).get(
		'/-Traces/|*v/-Samples/|Default'
	)

#/######################/#
# Print
#

#print
print('MyRecorder is ')
SYS._print(MyRecorder)

