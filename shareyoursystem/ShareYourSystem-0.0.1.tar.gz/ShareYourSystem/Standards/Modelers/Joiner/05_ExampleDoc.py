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
			{
				'-Models':[
					('|Parameter',[
						('ModelKeyStrsList',['MultiplyingFirstFloat','MultiplyingSecondFloat'])
					]),
					('|Result',{
						'ModelKeyStrsList':['MultipliedTotalFloat'],
						'-Jonctions':{
								'|/^/|Parameter':{}
							}
						}
					)
				]
			}
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
			{
				#COMPONENTS
				'-Components':{
					'|Real':MultiplierClass(),
					'|Image':MultiplierClass()
				},
				#MODELS
				'-Models':[
					('|Parameter',[
						('ModelKeyStrsList',['ModulingPowerFloat'])
					]),
					('|Result',{
						'ModelKeyStrsList':['ModuledTotalFloat'],
						'-Jonctions':{
								'<->/^/^/-Components/|Real/-Models/|Parameter':{},
								'<->/^/^/-Components/|Image/-Models/|Parameter':{}
							}
						}
					)
				]
			}
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
					self['/-Components/|Real'].multiply().MultipliedTotalFloat
				]
			)**self.ModulingPowerFloat

#/######################/#
# Build your total model and insert
#

MyModuler=ModulerClass(
		**{
			'FolderingPathVariable':SYS.Joiner.LocalFolderPathStr,
			'PymongoingDatabaseStr':'Modulus'
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
		'#call:insert'
	)
"""


#/######################/#
# Print
#

#print
print('mongo db is : \n'+SYS._str(MyModuler.pymongoview()))

#print
print('MyModuler is ')
SYS._print(MyModuler)

#Print
MyModuler.process(_ActionStr='kill')