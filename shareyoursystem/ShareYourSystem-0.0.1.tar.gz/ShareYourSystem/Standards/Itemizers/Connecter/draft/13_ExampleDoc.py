#/######################/#
# Import
#

#ImportModules
import ShareYourSystem as SYS

#/######################/#
# Define you hierarchic objects
#

#Define a Moduler class
@SYS.ClasserClass()
class MultiplierClass(SYS.ConnecterClass):
								
	def default_init(self,
						_MultiplyingFirstFloat=0,
						_MultiplyingSecondFloat=0,
						_MultipliedTotalFloat=0,
						**_KwargVariablesDict
					):

		#Call the parent init method
		SYS.ConnecterClass.__init__(self,**_KwargVariablesDict)
			
		#Build the model		
		self.mapSet(
			[
				('-Models',[
						('|Parameter',[
							('ModelKeyStrsList',['MultiplyingFirstFloat','MultiplyingSecondFloat'])
						]),
						('|Result',[
							('ModelKeyStrsList',['MultipliedTotalFloat']),
							('ParentingTriggerVariable',['<->/^/|Parameter'])
						])
					]
				)
			]
		)

#Define a Moduler class
@SYS.ClasserClass()
class ModulerClass(SYS.ConnecterClass):
								
	def default_init(self,
						_ModulingPowerFloat=0.5,
						_ModuledTotalFloat=0,
						**_KwargVariablesDict
					):

		#Call the parent init method
		SYS.ConnecterClass.__init__(self,**_KwargVariablesDict)

		#Build the components and the models
		self.mapSet(
			[
				#MODELS
				(
					'-Models',
					[
						('|Parameter',[
							('ModelKeyStrsList',['ModulingPowerFloat']),
							(
								'ParentingTriggerVariable',
								[
									'<->/^/^/-Components/|Real/-Models/|Result',
									'<->/^/^/-Components/|Image/-Models/|Result',
								]
							)
						]), 
						('|Result',[
							('ModelKeyStrsList',['ModuledTotalFloat']),
							(
								'ParentingTriggerVariable',
								[
									'<->/^/|Parameter'
								]
							)
						])
					]
				),
				#COMPONENTS
				(
					'-Components',{
						'|Real':MultiplierClass(),
						'|Image':MultiplierClass()
					}
				)
			]
		)
						
#/######################/#
# Build your total model and insert
#

MyModuler=ModulerClass(
	).parentDown()

#/######################/#
# Print
#

#print
print('MyModuler is ')
SYS._print(MyModuler)

