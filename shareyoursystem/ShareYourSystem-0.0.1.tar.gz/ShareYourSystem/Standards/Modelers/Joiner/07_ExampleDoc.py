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
class MultiplierClass(SYS.JoinerClass):
								
	def default_init(self,
						_MultiplyingFirstFloat=0,
						_MultiplyingSecondFloat=0,
						_MultipliedTotalFloat=0,
						**_KwargVariablesDict
					):

		#Call the parent init method
		SYS.JoinerClass.__init__(self,**_KwargVariablesDict)
			
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

	def do_multiply(self):
		
		#debug
		'''
		self.debug(('self.',self,['MultiplyingFirstFloat','MultiplyingSecondFloat']))
		'''

		#set the SumedTotalFloat
		self.MultipliedTotalFloat=self.MultiplyingFirstFloat*self.MultiplyingSecondFloat

#Define a Moduler class
@SYS.ClasserClass()
class ModulerClass(SYS.JoinerClass):
								
	def default_init(self,
						_ModulingPowerFloat=0.5,
						_ModuledTotalFloat=0,
						**_KwargVariablesDict
					):

		#Call the parent init method
		SYS.JoinerClass.__init__(self,**_KwargVariablesDict)

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
						
	def do_module(self):
		
		#debug
		'''
		self.debug(('self.',self,['SumingFirstFloat','SumingSecondFloat']))
		'''

		#set the SumedTotalFloat
		self.ModuledTotalFloat=sum(
				[
					self['/-Components/|Real'].multiply().MultipliedTotalFloat,
					self['/-Components/|Image'].multiply().MultipliedTotalFloat
				]
			)**self.ModulingPowerFloat

#/######################/#
# Build your total model and insert
#

#MyModuler
MyModuler=ModulerClass(
		**{
			'FolderingPathVariable':SYS.Joiner.LocalFolderPathStr,
			'HdformatingFileKeyStr':'Modulus.hdf5'
		}
	).model(
	).mapSet(
		{
			'/-Components/|Real':{
				'MultiplyingFirstFloat':3.,
				'MultiplyingSecondFloat':1.
			},
			'/-Components/|Image':{
				'MultiplyingFirstFloat':1.,
				'MultiplyingSecondFloat':2.
			}
		}
	).module(
	).command(
		'/-Models/|Result',
		[
			'#call:insert',
			('setSwitch',['insert'])
		]
	)

"""
	.mapSet(
		{
			'/-Components/|Real':{
				'MultiplyingFirstFloat':2.,
				'MultiplyingSecondFloat':2.
			},
			'/-Components/|Image':{
				'MultiplyingFirstFloat':1.,
				'MultiplyingSecondFloat':2.
			}
		}
	).module(
	).command(
		'/-Models/|Result',
		'#call:insert'
	)
"""

#/######################/#
# Print
#

#print
print('MyModuler is ')
SYS._print(MyModuler)

#view
print('hdf5 file is : \n'+SYS._str(MyModuler.hdfview()))

#close
MyModuler.file(_ModeStr='c')
