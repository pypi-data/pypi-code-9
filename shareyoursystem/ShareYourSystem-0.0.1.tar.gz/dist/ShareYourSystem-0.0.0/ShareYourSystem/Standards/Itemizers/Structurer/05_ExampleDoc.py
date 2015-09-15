#/######################/#
# Import
#

#ImportModules
import ShareYourSystem as SYS

#/######################/#
# Define you hierarchic objects
#

#add
SYS.addSingPlural('Component','Components')

#Define a Moduler class
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

#Define a Moduler class
@SYS.ClasserClass()
class ModulerClass(SYS.StructurerClass):
								
	def default_init(self,
						_ModulingPowerFloat=0.5,
						_ModuledTotalFloat=0,
						**_KwargVariablesDict
					):

		#Call the parent init method
		SYS.StructurerClass.__init__(self,**_KwargVariablesDict)

		#Build the components and the models
		self.mapSet(
			[
				#MODELS
				(
					'-Models',
					[
						('|Parameter',[
							('ModelKeyStrsList',['ModulingPowerFloat']),
							('StructureConnectPrefixStrsList',['Jonct']),
							(
								'array',[
									[
										['-Jonctions'],
										[
											'|/^/^/-Components/|Real/-Models/|Result',
											'|/^/^/-Components/|Image/-Models/|Result'
										]
									]
								]	
							),
						]), 
						('|Result',[
							('ModelKeyStrsList',['ModuledTotalFloat']),
							('ParentingTriggerVariable',['->/^/|Parameter'])
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
# Build your total model 
#

MyModuler=ModulerClass(
	).structure(
		#StructuringTeamerCommandKeyVariable					
		[
			'Components',
			'Models'
		],
		#StructuringManagerCommandKeyVariable
		"#all"
	)

#/######################/#
# Print
#

#print
print('MyModuler is ')
SYS._print(MyModuler)

