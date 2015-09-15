#/######################/#
# Import
#

#ImportModules
import ShareYourSystem as SYS

#/######################/#
# Define you hierarchic objects
#


#Define a Multiplier class
@SYS.ClasserClass()
class MultiplierClass(SYS.StructurerClass):
								
	def default_init(self,
						_MultiplyingFirstFloat=0,
						_MultiplyingSecondFloat=0,
						_MultipliedTotalFloat=0,
						**_KwargVariablesDict
					):

		#Call the parent init method
		SYS.StructurerClass.__init__(self,**_KwargVariablesDict)
			
		#Build the model		
		self.mapSet(
			[
				('-Models',[
						('|Parameter',[
							('ModelKeyStrsList',['MultiplyingFirstFloat','MultiplyingSecondFloat'])
						]),
						('|Result',[
							('ModelKeyStrsList',['MultipliedTotalFloat']),
							('ParentingTriggerVariable',['->/^/|Parameter'])
						])
					]
				)
			]
		)

#/######################/#
# Build your total model 
#

MyMultiplier=MultiplierClass(
	).structure(
		#StructuringTeamerCommandKeyVariable					
		[
			'Models'
		],
		#StructuringManagerCommandKeyVariable
		"#all"
	)

#/######################/#
# Print
#

#print
print('MyMultiplier is ')
SYS._print(MyMultiplier)

#print
print("\nMyMultiplier['/-Models/|Result'].ConnectedToVariable")
SYS._print(MyMultiplier['/-Models/|Result'].ConnectedToVariable)

