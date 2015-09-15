# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


A Leaker

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Recorders.Brianer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
SYS.addDo('Leaker','Leak','Leaking','Leaked')
#</DefineAugmentation>

#<ImportSpecificModules>
from ShareYourSystem.Standards.Interfacers import Printer
from ShareYourSystem.Standards.Recorders import Recorder
#</ImportSpecificModules>

#<DefineLocals>
LeakScalarPrefixStr='#scalar:'
LeakEquationPrefixStr='#equation:'
LeakCustomPrefixStr='#custom:'
LeakClockPrefixStr='#clock:'
LeakNetworkPrefixStr='#network:'
LeakActivityPrefixStr="U"
LeakInputPrefixStr="I"
LeakInteractionPrefixStr="J"

#define
def detectThreshold(_VariablesList,_PopulationDeriveLeaker):

	#set
	SpikeArray = _VariablesList['_spikespace']
	ActivityArray = _VariablesList[
				_PopulationDeriveLeaker.LeakedSymbolStr
			]
	
	#Choose
	AboveArray=(ActivityArray > _PopulationDeriveLeaker.LeakingThresholdVariable).nonzero()[0]

	#Debug
	print('l 52 detectThreshold')
	print('SpikeArray is ')
	print(SpikeArray)
	print('AboveArray is')
	print(AboveArray)
	print('')

def getShapeArray(_Variable,_RowsInt,_ColsInt):

	#import
	import numpy as np 

	#shape
	ShapeTuple=np.shape(_Variable)

	#Check
	if len(ShapeTuple)!=2:

		#reshape
		return np.reshape(
			np.array(
				_Variable
			),
			(_RowsInt,_ColsInt)
		)

	else:
		
		#alias
		return _Variable


"""
def filterSpike(_VariablesList,_ActivityStr,_ThresholdVariable):

	#set
	SpikeArray = _VariablesList['_spikespace']
	ActivityArray = _VariablesList[
				_ActivityStr
			]
	
	#Choose
	AboveArray=(ActivityArray > _ThresholdVariable).nonzero()[0]

	#Check
	if len(AboveArray):
		# only let one neuron spike
		SpikeArray[0] = AboveArray[0]
		SpikeArray[-1] = 1
	else:
		SpikeArray[-1] = 0
"""


#</DefineLocals>

#<DefineClass>
@DecorationClass(**{
	'ClassingSwitchMethodStrsList':['leak'],
	'ClassingStructureVariable':[
			('Population','Populations'),
			('Trace','Traces'),
			('Sample','Samples'),
			('Event','Events'),
			('Interactome','Interactomes'),
			('Interaction','Interactions'),
			('Input','Inputs')
		]
})
class LeakerClass(BaseClass):
		
	def default_init(self,
			_LeakingUnitsInt=0,
			_LeakingTimeVariable='#scalar:10.*ms',
			_LeakingWeigthVariable=None,
			_LeakingQuantityStr='mV',
			_LeakingMonitorIndexIntsList=None,
			_LeakingSymbolPrefixStr="",
			_LeakingInteractionStr="Rate",
			_LeakingVariableStr="",
			_LeakingTransferVariable=None,
			_LeakingThresholdVariable=None,
			_LeakingResetVariable=None,
			_LeakingRecordBool=False,
			_LeakingNoiseStdVariable=None,
			_LeakingDelayVariable=None,
			_LeakingPlasticVariable=None,
			_LeakingGlobalBool=False,
			_LeakedRecordSkipStrsList=None,
			_LeakedQuantityVariable=None,
			_LeakedDimensionStr="",
			_LeakedModelStr="",
			_LeakedCurrentStr="",
			_LeakedClampStr="",
			_LeakedSymbolStr="",
			_LeakedOperationStr="",
			_LeakedEquationStr="",
			_LeakedClockStr="",
			_LeakedTimeSymbolStr="",
			_LeakedInteractionWeigthFloat=0.,
			_LeakedParentSingularStr="",
			_LeakedParentNetworkDeriveLeakerVariable=None,
			_LeakedParentPopulationDeriveLeakerVariable=None,
			_LeakedParentInteractomeDeriveLeakerVariable=None,
			_LeakedTimedArrayVariable=None,
			_LeakedVariableStr="",
			_LeakedDelayTimeFloat=0.,
			_LeakedDelayTimeInt=0,
			_LeakedMinFloat=0.,
			_LeakedMaxFloat=0.,
			#_LeakedGlobalSynapsesVariable=None,
			_LeakedMeanStateMonitorVariable=None,
			_LeakedVarStateMonitorVariable=None,
			'LeakedMeanFloatsArray',
			'LeakedStdFloatsArray'
			**_KwargVariablesDict
		):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_leak(self):

		#/#################/#
		# Determine if it is an inside structure or the top
		#

		#debug
		'''
		self.debug(
			[
				'We leak here',
				'First look for deeper teams in the structure',
			]
		)
		'''

		#Check
		if self.ParentedTotalSingularListDict!=None and len(
			self.ParentedTotalSingularListDict
		)>0:

			#debug
			'''
			self.debug(
				[
					'self.ParentedTotalSingularListDict.keys() is ',
					str(self.ParentedTotalSingularListDict.keys())
				]
			)
			'''

			#get
			self.LeakedParentSingularStr=self.ParentedTotalSingularListDict.keys()[0]

		#debug
		'''
		self.debug(
			[
				'Ok',
				('self.',self,['LeakedParentSingularStr'])
			]
		)
		'''

		#Check
		if (self.ParentDeriveTeamerVariable==None or 'Populations' in self.TeamDict or self.ParentDeriveTeamerVariable.TeamTagStr not in [
			'Traces',
			'Samples',
			'Events',
			'Interactomes',
			'Interactions',
			'Inputs'
		]) and self.LeakedParentSingularStr!='Population':

			#/########################/#
			# Network level
			# 

			#debug
			'''
			self.debug(
				[
					'It is a Network level for the leak',
				]
			)
			'''

			#/########################/#
			# structure leak the interactions
			# 

			#debug
			'''
			self.debug(
				[
					'We structure filterLeak all the interacting children...'
					'So we pass thrugh the populations and leak the interactomes, interactions and inputs',
				]
			)	
			'''

			#/########################/#
			# leakNetwork
			#

			#leakNetwork
			self.leakNetwork()

			#set
			self.StructureFilterTeamTagStrsList=[
				'Populations'
			]

			#structure
			self.structure(
				[
					'Populations',
					'Inputs',
					'Interactomes',
					'Interactions',
				],
				'#all',
				_ManagerCommandSetList=[
					'filterLeak'
				]
			)

			#debug
			'''
			self.debug(
				[
					'Ok we have structured the interacting children',
					'Now we brian Network'
				]
			)
			'''

			#/########################/#
			# brianNetwork
			#

			#brian
			self.brianNetwork()

			#/########################/#
			# Special Network-Neurongroup level
			# 

			#Check
			if 'Populations' not in self.TeamDict:
		
				#debug
				'''
				self.debug(
					[
						'...But there is no population',
						'so set a leak model here '
					]
				)
				'''

				#leakPopulation
				self.leakPopulation()

				#debug
				'''
				self.debug(
					[
						'Ok we have leak setted the population',
						'Now we also brianPopulation'
					]
				)
				'''

				#brianPopulation
				self.brianPopulation()

				#debug
				'''
				self.debug(
					[
						'Ok we have brian setted the population'
					]
				)
				'''

			#/########################/#
			# structure leak
			# 

			#debug
			'''
			self.debug(
				[
					'We structure leak brian all the children...',
					'self.TeamDict.keys() is ',
					str(self.TeamDict.keys()),
					'but map brian Clock first'
				]
			)
			'''

			#set
			self.StructureFilterTeamTagStrsList=None

			#map brian clock first
			map(
				lambda __DeriveBrianer:
				__DeriveBrianer.brianClock(),
				self.TeamDict["Clocks"].ManagementDict.values()
			)

			#structure
			self.structure(
				[
					'Populations',
					'Traces',
					'Samples',
					'Events',
					'Interactomes',
					'Interactions',
				],
				'#all',
				_ManagerCommandSetList=['leak','brian']
			)

			#debug
			'''
			self.debug(
				[
					'Ok we have structured leak brian all the children',
				]
			)
			'''

		else:

			#/########################/#
			# Inside structure
			#

			#debug
			'''
			self.debug(
				[
					'Ok we check if this parentsingular has a special method ',
					('self.',self,[
						'LeakedParentSingularStr'
					])
				]
			)
			'''

			#set
			LeakedMethodKeyStr='leak'+self.LeakedParentSingularStr

			#Check
			if hasattr(self,LeakedMethodKeyStr):

				#/########################/#
				# call the special leak<LeakedParentSingularStr> method
				#

				#debug
				'''
				self.debug(
					[
						'It is a '+self.LeakedParentSingularStr+' level',
						'We leak<LeakedParentSingularStr>'
					]
				)
				'''

				#call
				getattr(
					self,
					LeakedMethodKeyStr
				)()

				#debug
				'''
				self.debug(
					[
						'Ok we have setted leak'+self.LeakedParentSingularStr
					]
				)
				'''	
		
	def leakNetwork(self):

		#/################/#
		# nothing here it is just a derive possible hook for derived classes
		#

		#debug
		'''
		self.debug(
			[
				'I a m just a possible hook for later derived classes'
			]
		)
		'''

		#pass
		pass

	def leakPopulation(self):

		#/################/#
		# Check the SymbolStr DimensionStr
		#

		#Check
		if self.LeakingSymbolPrefixStr=="":
			self.LeakingSymbolPrefixStr=LeakActivityPrefixStr

		#set direct
		self.LeakedSymbolStr=self.LeakingSymbolPrefixStr

		#Check
		if self.LeakedQuantityVariable==None:
			self.setDimension()

		#debug
		'''
		self.debug(
			[
				'We leak population here',
				('self.',self,[
					'LeakingQuantityStr',
					'LeakedQuantityVariable',
					'LeakedDimensionStr'
				])
			]
		)
		'''

		#/################/#
		# Look for the time constant
		#

		#debug
		'''
		self.debug(
			[
				'We set a population here',
				'look for the time constant',
				('self.',self,[
						'LeakingTimeVariable'
					])
			]
		)
		'''

		#Check
		if type(
			self.LeakingTimeVariable
		)==str:

			#Check
			if self.LeakingTimeVariable.startswith(LeakScalarPrefixStr):

				#set
				self.LeakedClampStr="Scalar"

				#debug
				'''
				self.debug(
					[
						'We direct write the time constant as a scalar in the equation'
					]
				)
				'''

				#set
				self.LeakedTimeSymbolStr=SYS.deprefix(
					self.LeakingTimeVariable,
					LeakScalarPrefixStr
				)

		else:

			#set
			self.LeakedClampStr="Variable"

			#debug
			'''
			self.debug(
				[
					'The time constant is seen as a variable with a specific name'
				]
			)
			'''

			#Check
			if self.LeakingTimeVariable!=0.:

				#set
				self.LeakedTimeSymbolStr="tau_"+self.LeakingSymbolPrefixStr

				#append
				self.LeakedRecordSkipStrsList.append(self.LeakedTimeSymbolStr)

				#define the time constant variable
				self.LeakedModelStr+=self.LeakedTimeSymbolStr+' : second\n'

		#/################/#
		# Define the main leak equation
		#

		#debug
		'''
		self.debug(
			[
				'We define the main leak equation but maybe it is just a direct value',
				('self.',self,[
					'LeakingTimeVariable'
				])
			]
		)
		'''

		#Check
		LeakedDirectVariableBool=False
		if self.LeakedClampStr=="Scalar":
			if float(self.LeakedTimeSymbolStr.split('*')[0])==0.:
				LeakedDirectVariableBool=True

		#Check
		if self.LeakingTimeVariable==0 or LeakedDirectVariableBool:

			#debug
			'''
			self.debug(
				[
					'Time constant is null',
					'Build just a variable definition clamped to the current',
					('self.',self,[
						'LeakingTimeVariable',
						'LeakedCurrentStr',
						'LeakedDimensionStr'
					])
				]
			)
			'''

			#set the left 
			self.LeakedModelStr+=self.LeakingSymbolPrefixStr

			#add
			self.LeakedModelStr+='='+self.LeakedCurrentStr

			#add
			self.LeakedModelStr+=' : '+self.LeakedDimensionStr+"\n"

		else:

			#debug
			'''
			self.debug(
				[
					'Build a differential equation',
					('self.',self,[
							'LeakedModelStr'
						])
				]	
			)
			'''

			#set the left 
			self.LeakedModelStr+="d"+self.LeakedSymbolStr+'/dt='

			#debug
			'''
			self.debug(
				[
					'Check if we add a weigth',
					('self.',self,[
							'LeakingWeigthVariable'
						])
				]
			)
			'''

			#type
			LeakedType=type(self.LeakingWeigthVariable)

			#Check
			if LeakedType==str:

				#Check
				if self.LeakingWeigthVariable in ['0','0.0']:

					#set the right
					self.LeakedModelStr+='('

				else:

					#set the right
					self.LeakedModelStr+='(-'+self.LeakingWeigthVariable+'*'+self.LeakedSymbolStr

			elif LeakedType in [list]:

				#link
				self.LeakedModelStr='''
					mu : 1
				'''+self.LeakedModelStr

			elif self.LeakingWeigthVariable!=None:

				#set the right
				self.LeakedModelStr+='(-'+str(
					self.LeakingWeigthVariable
				)+'*'+self.LeakedSymbolStr

			else:

				#set the right
				self.LeakedModelStr+='(-'+self.LeakedSymbolStr

			#debug
			'''
			self.debug(
				[
					'We maybe add a current',
					('self.',self,[
							'LeakedCurrentStr'
						])
				]
			)
			'''

			#Check
			if self.LeakedCurrentStr!="":

				#debug
				'''
				self.debug(
					[
						'We maybe transfer',
						('self.',self,[
								'LeakingTransferVariable',
								'LeakedModelStr'
							])
					]
				)
				'''

				#Check
				if self.LeakedModelStr[-1]!='(':
					self.LeakedModelStr+='+'

				#Check
				if self.LeakingTransferVariable!=None:

					#Check
					if type(
						self.LeakingTransferVariable
					)==str:

						#debug
						'''
						self.debug(
							[
								'It is a str transfer',
								'We put it in the model and replace the #CurrentStr by self.LeakedCurrentStr',
								('self.',self,[
									'LeakedCurrentStr'
								])
							]
						)
						'''

						#add
						self.LeakedModelStr+=self.LeakingTransferVariable.replace(
								'#CurrentStr',
								self.LeakedCurrentStr
							)

					else:

						#debug
						'''
						self.debug(
							[
								'It is a function transfer'
							]
						)
						'''

						#add
						self.LeakedModelStr+='F('+self.LeakedCurrentStr+')'

				else:

					#debug
					'''
					self.debug(
						[
							'We add directly the leaked current'
						]
					)
					'''

					#Check
					self.LeakedModelStr+=self.LeakedCurrentStr

			#debug
			'''
			self.debug(
				[
					'We divide by the time',
					('self.',self,[
						'LeakedClampStr'
					])
				]
			)
			'''


			#Check
			if self.LeakingNoiseStdVariable!=None:

				#Check
				self.LeakedModelStr+='+'

				if type(self.LeakingNoiseStdVariable)==str:

					#add
					self.LeakedModelStr+=self.LeakingNoiseStdVariable

				else:

					#str
					self.LeakedModelStr+=str(
						self.LeakingNoiseStdVariable
					)+'*'+str(self.LeakedQuantityVariable)

			#Check
			if self.LeakingNoiseStdVariable!=None:

				#add
				self.LeakedModelStr+='*sqrt('+self.LeakedTimeSymbolStr+')*xi'

			#set
			self.LeakedModelStr+=')'

			#set the right denominator
			if self.LeakedClampStr in ["Scalar","Variable"]:

				#add
				self.LeakedModelStr+='/('+self.LeakedTimeSymbolStr+')'

			#set the dimension
			self.LeakedModelStr+=' : '+self.LeakedDimensionStr+"\n"

		#debug
		'''
		self.debug(
			[
				'We have defined the leak model str',
				('self.',self,[
					'LeakedModelStr'
				])
			]
		)
		'''

		#/################/#
		# Now update the Traces
		#

		#team traces
		LeakedTracesDeriveManager=self.team(
			'Traces'
			).TeamedValueVariable

		#manage
		LeakedRecordDeriveLeaker=LeakedTracesDeriveManager.manage(
				'*'+self.LeakedSymbolStr
			).ManagedValueVariable

		#set
		LeakedRecordDeriveLeaker.NumscipyingStdFloat=0.001
		LeakedSamplesDeriveLeaker=LeakedRecordDeriveLeaker.team(
				'Samples'
			).TeamedValueVariable
		LeakedDefaultDeriveLeaker=LeakedSamplesDeriveLeaker.manage(
				'Default'
			).ManagedValueVariable

		#/##################/#
		# Look for what to monitor
		#

		#Check
		if self.RecordingLabelVariable!=None:

			#alias
			LeakedDefaultDeriveLeaker.RecordingLabelVariable=self.RecordingLabelVariable
		else:

			#debug
			'''
			self.debug(
				[
					'Check the monitor indexes',
					('self.',self,[
							'LeakingMonitorIndexIntsList',
							'LeakingUnitsInt'
						])
				]
			)
			'''

			#Check
			if len(self.LeakingMonitorIndexIntsList
				)==0:

				#set
				self.LeakingMonitorIndexIntsList=[0]
				
			elif len(
				self.LeakingMonitorIndexIntsList
			)>self.LeakingUnitsInt:

				#set
				self.LeakingMonitorIndexIntsList=self.LeakingMonitorIndexIntsList[:self.LeakingUnitsInt]

			#set
			LeakedDefaultDeriveLeaker.RecordingLabelVariable=self.LeakingMonitorIndexIntsList

		#/##################/#
		# Init the Neurongroup dict
		#

		#init
		BrianingNeurongroupDict={
				}

		#/##################/#
		# Look for a Threshold 
		#

		#debug
		'''
		self.debug(
			[
				'Look for a threshold',
				('self.',self,[
					'LeakingThresholdVariable'
				])
			]
		)
		'''

		#Check
		if type(self.LeakingThresholdVariable)!=None.__class__:

			#type
			LeakedType=type(self.LeakingThresholdVariable)

			#Check
			if LeakedType==str:

				#Check
				if self.LeakingThresholdVariable.startswith(LeakScalarPrefixStr):

					#debug
					'''
					self.debug(
						[
							'It is a scalar threshod'
						]
					)
					'''

					#set
					BrianingNeurongroupDict['threshold']=SYS.deprefix(
						self.LeakingThresholdVariable,
						LeakScalarPrefixStr
					)

			else:

				#import 
				import numpy as np

				#Check
				if LeakedType in [list,np.ndarray,float,np.float64]:

					#debug
					'''
					self.debug(
						[
							'It is a variable threshod',
							'add in the model'
						]
					)
					'''

					#Define
					self.LeakedModelStr+='Threshold : '+self.LeakedDimensionStr+"\n"

					#set
					BrianingNeurongroupDict['threshold']=self.LeakedSymbolStr+'>Threshold'
					
				else:
	
					#debug
					'''
					self.debug(
						[
							'It is a CodeObject threshod',
							'add in the model'
						]
					)
					'''

					#import
					from brian2 import CodeObject

					#define
					def ThresholdFunction(_VariablesList):

						#map
						map(
							lambda __Method:
							__Method(
								_VariablesList,
								self
							),
							self.LeakingThresholdVariable['MethodsList']
						)


					#Init
					ThresholdCodeObject = CodeObject()(
							ThresholdFunction,
					    	uses_variables=[
					    		'_spikespace',
					    		self.LeakedSymbolStr
					    	]
					    )
				
		#/##################/#
		# Look for a Reset
		#

		#debug
		'''
		self.debug(
			[
				'Look for a reset',
				('self.',self,[
					'LeakingResetVariable'
				])
			]
		)
		'''

		#Check
		if self.LeakingResetVariable!=None:

			#Check
			if type(self.LeakingResetVariable)==str:

				#Check
				if self.LeakingResetVariable.startswith(LeakScalarPrefixStr):

					#debug
					'''
					self.debug(
						[
							'It is a scalar reset'
						]
					)
					'''

					#set
					BrianingNeurongroupDict['reset']=SYS.deprefix(
						self.LeakingResetVariable,
						LeakScalarPrefixStr
					)

			else: 

				#import 
				import numpy

				#Check
				if type(self.LeakingResetVariable) in [float,numpy.float64]:

					#set
					BrianingNeurongroupDict['reset']=self.LeakedSymbolStr+"="+str(
						self.LeakingResetVariable
					)+'*'+str(
						self.LeakedQuantityVariable
					)

		"""
		#/##################/#
		# Is there a global variable to compute
		#

		#Check
		if self.LeakingGlobalBool:

			#debug
			self.debug(
				[
					'We compute a global statistical variables',
					('self.',self,[
							'LeakedModelStr'
						])
				]
			)

			#add
			self.LeakedModelStr+='Mean_'+self.LeakedSymbolStr +' : '+self.LeakedDimensionStr

			#add
			self.LeakedModelStr+='\n'+'Var_'+self.LeakedSymbolStr +' : 1'

			#debug
			self.debug(
				[
					'In the end',
					('self.',self,[
							'LeakedModelStr'
						])
				]
			)
		"""

		#/##################/#
		# Set the neurongroup dict
		#

		#debug
		'''
		self.debug(
			[
				'Set the BrianingNeurongroupDict',
				('self.',self,[
						'LeakingUnitsInt'
						]
				)
			]
		)
		'''
		
		#set
		BrianingNeurongroupDict['N']=self.LeakingUnitsInt
		BrianingNeurongroupDict['model']=self.LeakedModelStr

		#Check
		if self.BrianingNeurongroupDict==None:
		
			#init
			self.BrianingNeurongroupDict=BrianingNeurongroupDict

		else:

			#update
			self.BrianingNeurongroupDict.update(
				BrianingNeurongroupDict
			)

		#debug
		'''
		self.debug(
			[
				'We have aliased the BrianingNeurongroupDict',
				('self.',self,[
						'BrianingNeurongroupDict'
					])
			]
		)
		'''




	def leakTrace(self):

		#/#################/#
		# Determine the parent
		#

		#set
		self.LeakedParentPopulationDeriveLeakerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

		#/#################/#
		# If this a trace with a threshold
		# then center the random pick around it

		#Check
		if hasattr(
			self.LeakedParentPopulationDeriveLeakerVariable.BrianedNeurongroupVariable,
			'Threshold'
		):

			#Check
			if self.RecordKeyStr==self.LeakedParentPopulationDeriveLeakerVariable.LeakedSymbolStr:

				#debug
				'''
				self.debug(
					[
						'We init under the thresholds',
						('self.',self,[
								'ManagementTagStr',
								'RecordKeyStr'
							]),
						'self.LeakedParentPopulationDeriveLeakerVariable.LeakingThresholdVariable is',
						str(self.LeakedParentPopulationDeriveLeakerVariable.LeakingThresholdVariable)
					]
				)
				'''
				
				#type
				LeakedThresholdType=type(self.LeakedParentPopulationDeriveLeakerVariable.LeakingThresholdVariable)

				#import
				import numpy as np

				#Check
				if LeakedThresholdType in [float,np.float64]:
					self.LeakedMaxFloat=self.LeakedParentPopulationDeriveLeakerVariable.LeakingThresholdVariable
				else:
					self.LeakedMaxFloat=self.LeakedParentPopulationDeriveLeakerVariable.LeakingThresholdVariable.min()

				#set
				self.NumscipyingMeanFloat=self.LeakedMaxFloat

				#debug
				'''
				self.debug(
					[
						'Mean is then around',
						('self.',self,[
								'NumscipyingMeanFloat'
							])
					]
				)
				'''

	def leakInput(self):

		#/################/#
		# Input level
		#

		#debug
		'''
		self.debug(
			[
				'It is an Input level',
			]
		)
		'''

		#Check
		if self.LeakingSymbolPrefixStr=="":
			self.LeakingSymbolPrefixStr=LeakInputPrefixStr

		#/################/#
		# Determine the parent
		#

		#set
		self.LeakedParentPopulationDeriveLeakerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

		#Check
		if self.LeakedParentPopulationDeriveLeakerVariable.ParentDeriveTeamerVariable!=None:

			#get
			self.LeakedParentNetworkDeriveLeakerVariable=self.LeakedParentPopulationDeriveLeakerVariable.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

		else:

			#get
			self.LeakedParentNetworkDeriveLeakerVariable=self.LeakedParentPopulationDeriveLeakerVariable


		#/################/#
		# Add in the model
		#

		#set
		self.LeakedSymbolStr=self.LeakingSymbolPrefixStr+self.ParentTagStr.split(
			'Inputs'
		)[-1].replace(
			'/','_'
		)

		#debug
		'''
		self.debug(
			[
				'we add in the model of the parent population',
				('self.',self,['LeakedSymbolStr']),
				'self.LeakedParentPopulationDeriveLeakerVariable.LeakedCurrentStr is ',
				self.LeakedParentPopulationDeriveLeakerVariable.LeakedCurrentStr
			]
		)
		'''

		#Check
		if self.LeakingWeigthVariable!=None:

			#Check
			if type(self.LeakingWeigthVariable)==str:

				#Check
				if self.LeakingWeigthVariable.startswith(LeakScalarPrefixStr):

					#set
					self.LeakedClampStr="Scalar"

					#set
					self.LeakedSymbolStr=SYS.deprefix(
						self.LeakingWeigthVariable,
						LeakScalarPrefixStr
					)

					#debug
					'''
					self.debug(
						[
							'It is an external scalar so just add Current',
							"self.LeakedParentPopulationDeriveLeakerVariable.LeakedModelStr is ",
							self.LeakedParentPopulationDeriveLeakerVariable.LeakedModelStr
						]
					)
					'''

					#add in the current
					self.LeakedParentPopulationDeriveLeakerVariable.addCurrentStr(
						self.LeakedSymbolStr
					)

				elif self.LeakingWeigthVariable.startswith(LeakEquationPrefixStr):

					#set
					self.LeakedClampStr='Equation'

					#set
					self.LeakedOperationStr=SYS.deprefix(
						self.LeakingWeigthVariable,
						LeakEquationPrefixStr
					)

					#setOperation
					self.setOperation()

				elif self.LeakingWeigthVariable.startswith(LeakCustomPrefixStr):

					#set
					self.LeakedClampStr='Custom'

					#set
					self.LeakedOperationStr=SYS.deprefix(
						self.LeakingWeigthVariable,
						LeakCustomPrefixStr
					)

					#setOperation
					self.setOperation()
		

				"""
				else:

					#debug
					'''
					self.debug(
						[
							'It is an external array so direct add plus a (t)'
						]
					)
					'''

					#Check
					if self.LeakedParentPopulationDeriveLeakerVariable.LeakedQuantityVariable==None:
						self.LeakedParentPopulationDeriveLeakerVariable.setDimension()

					#define in the model
					self.LeakedParentPopulationDeriveLeakerVariable.LeakedModelStr+=self.LeakedSymbolStr+' : '+self.LeakedParentPopulationDeriveLeakerVariable.LeakedDimensionStr+"\n"
					
					#add in the current
					self.LeakedParentPopulationDeriveLeakerVariable.addCurrentStr(
						#self.LeakedSymbolStr+'(t)'
						self.LeakedSymbolStr
					)
				"""

			#Check
			elif type(self.LeakingWeigthVariable) in [list,tuple]:

				#Check
				if self.LeakingWeigthVariable[0].startswith(LeakNetworkPrefixStr):

					#debug
					'''
					self.debug(
						[
							'It is a network operation',
							('self.',self,[
									'LeakingWeigthVariable'
								])
						]
					)
					'''

					#set
					self.LeakedClampStr='Network'

					#set
					self.LeakedOperationStr=SYS.deprefix(
						self.LeakingWeigthVariable[0],
						LeakNetworkPrefixStr
					)

					#setOperation
					self.setOperation()

			else:

				#set
				self.LeakedClampStr="Variable"

				#debug
				'''
				self.debug(
					[
						'It is a variable',
						('self.',self,[
								'LeakedSymbolStr'
							]),
						'We append in the parent pop record skip',
						'We define and add in the LeakedCurrentStr'
					]
				)
				'''

				#Check
				if self.LeakingRecordBool==False:

					#debug
					'''
					self.debug(
						[
							'we skip record this input'
						]
					)
					'''

					#append
					if self.LeakedParentPopulationDeriveLeakerVariable.LeakedRecordSkipStrsList==None:
						self.LeakedParentPopulationDeriveLeakerVariable.LeakedRecordSkipStrsList=[
							self.LeakedSymbolStr
						]
					else:
						self.LeakedParentPopulationDeriveLeakerVariable.LeakedRecordSkipStrsList.append(
							self.LeakedSymbolStr
						)

				#Check
				if self.LeakedParentPopulationDeriveLeakerVariable.LeakedQuantityVariable==None:
					self.LeakedParentPopulationDeriveLeakerVariable.setDimension()

				#define in the model
				self.LeakedParentPopulationDeriveLeakerVariable.LeakedModelStr+=self.LeakedSymbolStr+' : '+self.LeakedParentPopulationDeriveLeakerVariable.LeakedDimensionStr+"\n"
				
				#add in the current
				self.LeakedParentPopulationDeriveLeakerVariable.addCurrentStr(
					self.LeakedSymbolStr
				)

			#debug
			'''
			self.debug(
				[
					'In the end',
					"self.LeakedParentPopulationDeriveLeakerVariable.LeakedCurrentStr is ",
					self.LeakedParentPopulationDeriveLeakerVariable.LeakedCurrentStr,
					"self.LeakedParentPopulationDeriveLeakerVariable.LeakedModelStr is ",
					self.LeakedParentPopulationDeriveLeakerVariable.LeakedModelStr,
					('self.',self,[
							'LeakedSymbolStr'
						])
				]
			)
			'''

	def leakInteraction(self):

		#/################/#
		# Interaction level
		#

		#debug
		'''
		self.debug(
			[
				'It is an Interaction level',
				('self.',self,[
						'LeakingWeigthVariable'
					])
			]
		)
		'''

		#/####################/#
		# Determine the parent
		#

		#Check
		if self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable.LeakedParentSingularStr=='Projectome':

			#debug
			'''
			self.debug(
				[
					'We are in a interactome structure'
				]
			)
			'''

			#set
			self.LeakedParentProjectomeDeriveLeakerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

			#get
			self.LeakedParentPopulationDeriveLeakerVariable=self.LeakedParentProjectomeDeriveLeakerVariable.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

		else:

			#debug
			'''
			self.debug(
				[
					'There is no interactome structure'
				]
			)
			'''

			#get
			self.LeakedParentPopulationDeriveLeakerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

		#Check
		if self.LeakedParentPopulationDeriveLeakerVariable.ParentDeriveTeamerVariable!=None:

			#get
			self.LeakedParentNetworkDeriveLeakerVariable=self.LeakedParentPopulationDeriveLeakerVariable.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

		else:

			#get
			self.LeakedParentNetworkDeriveLeakerVariable=self.LeakedParentPopulationDeriveLeakerVariable

		#/####################/#
		# Maybe we have to connect
		#

		#Check
		if self.ConnectedToVariable==None:

			#debug
			'''
			self.debug(
				[
					'We setConnection here',
					('self.',self,[
							'ManagementTagStr',
							'ConnectingKeyVariable'
						])
				]
			)
			'''

			#setConnection
			self.setConnection(
				self.ManagementTagStr
				if self.ConnectingKeyVariable==None
				else self.ConnectingKeyVariable,
				self,
				self.LeakedParentPopulationDeriveLeakerVariable
			)

		#Check
		if self.ConnectedToVariable==None:

			#return
			return
			
		#Check
		if self.ConnectedToVariable.LeakedDimensionStr=="":
			self.ConnectedToVariable.setDimension()

		#/####################/#
		# Check the clamp of the interaction
		#

		#debug
		'''
		self.debug(
			[
				'What is LeakingWeigthVariable',
				('self.',self,[
						'LeakingWeigthVariable'
					])
			]
		)
		'''
		
		#Check
		if type(self.LeakingWeigthVariable)==None.__class__:

			#set
			self.LeakingWeigthVariable='#scalar:0.'

			#debug
			'''
			self.debug(
				[
					'We set a default J equal to scalar 0',
					('self.',self,[
							'LeakingWeigthVariable'
						])
				]
			)
			'''

		#debug
		'''
		self.debug(
			[
				'We check the clamp of the interaction',
				('self.',self,[
					'LeakingWeigthVariable'
				])
			]
		)
		'''

		#/##################/#
		# Check that the ConnectedToVariable has already its LeakedSymbolStr
		#

		#Check
		if self.ConnectedToVariable.LeakingSymbolPrefixStr=="":
			self.ConnectedToVariable.LeakingSymbolPrefixStr=LeakActivityPrefixStr
			self.ConnectedToVariable.LeakedSymbolStr=LeakActivityPrefixStr
		else:
			self.ConnectedToVariable.LeakedSymbolStr=self.ConnectedToVariable.LeakingSymbolPrefixStr

		#/##################/#
		# Look if it is Scalar or Variable interaction
		#

		#init
		self.LeakedClampStr="Variable"

		#Check
		if type(self.LeakingWeigthVariable)==str:

			#Check
			if self.LeakingWeigthVariable.startswith(
				LeakScalarPrefixStr
			):

				#debug
				'''
				self.debug(
					[
						'It is a scalar constant connection'
					]
				)
				'''

				#set
				self.LeakedClampStr="Scalar"


		#/##################/#
		# Choose the variable in the pre to be clamp in the post
		#

		#Check
		if self.LeakingSymbolPrefixStr=="":

			#debug
			'''
			self.debug(
				[
					'There is no LeakingSymbolPrefixStr here',
					'So we set it to the LeakInteractionPrefixStr'
				]
			)
			'''

			#set
			self.LeakingSymbolPrefixStr=LeakInteractionPrefixStr

		
		#/####################/#
		# Write the LeakedSymbolStr
		#

		#debug
		'''
		self.debug(
			[
				'We set the LeakedSymbolStr',
				('self.',self,[
					'LeakingSymbolPrefixStr'
				]),
				'self.ConnectedToVariable.LeakedSymbolStr is ',
				self.ConnectedToVariable.LeakedSymbolStr
			]
		)
		'''

		#set
		self.LeakedSymbolStr=self.LeakingSymbolPrefixStr

		#split
		self.LeakedSymbolStr+=self.ParentTagStr.split(
			'Interactions'
		)[-1].replace(
			'/',
			'_'
		)

		#debug
		'''
		self.debug(
			[
				'We add a suffix corresponding to the observed variable',
				('self.',self,[
						'LeakingVariableStr'
					])
			]
		)
		'''

		#Check
		if self.LeakingVariableStr=="":

			#Check
			if self.LeakingInteractionStr=="Rate":

				#debug
				'''
				self.debug(
					[
						'It is a rate interaction',
						'So the LeakedVariableStr has to be the ConnectedToVariable.LeakedSymbolStr by default'
					]
				)
				'''

				#add
				self.LeakedSymbolStr+=self.ConnectedToVariable.LeakedSymbolStr

				#Check
				self.LeakedVariableStr=self.ConnectedToVariable.LeakedSymbolStr

			"""
			elif self.LeakingInteractionStr=="Spike":

				#debug
				self.debug(
					[
						'It is a spike interaction',
						'So the LeakedVariableStr has to be the J'
					
					]
				)

				#add
				self.LeakedSymbolStr+='delta'

				#Check
				self.LeakedVariableStr=self.LeakingSymbolPrefixStr
			"""

		else:

			#add
			self.LeakedSymbolStr+=self.LeakingVariableStr
			self.LeakedVariableStr=self.LeakingVariableStr

		#/####################/#
		# Say that the ConnectedToVariable has to record skip this variable
		#

		#Check
		if self.LeakedClampStr=="Variable":

			#debug
			'''
			self.debug(
				[
					'It is a variable',
					('self.',self,[
							'LeakedSymbolStr'
						]),
					'We append in the ConnectedToVariable',
				]
			)
			'''

			#Check
			if self.LeakingRecordBool==False:

				#debug
				'''
				self.debug(
					[
						'we skip record this interaction'
					]
				)
				'''

				#append
				if self.ConnectedToVariable.LeakedRecordSkipStrsList==None:

					#init
					self.ConnectedToVariable.LeakedRecordSkipStrsList=[
						self.LeakedSymbolStr
					]
				else:

					#append
					self.ConnectedToVariable.LeakedRecordSkipStrsList.append(
						self.LeakedSymbolStr
					)


			#debug
			'''
			self.debug(
				[
					'in the end',
					('self.',self,[
						'LeakedSymbolStr'
					])
				]
			)
			'''

		#/####################/#
		# Build the interaction model
		#

		#debug
		'''
		self.debug(
			[
				'First we set the model in the synapse',
				('self.',self,[
					'LeakedClampStr'
				])
			]
		)
		'''

		#Check
		if self.LeakedClampStr=="Variable":

			#define
			self.LeakedModelStr+="\n"+self.LeakingSymbolPrefixStr+" : 1 \n"

		#Check
		if self.LeakingInteractionStr=="Rate":

			#set
			if self.LeakedClampStr=="Scalar":

				#debug
				'''
				self.debug(
					[
						'The interaction is a scalar',
						'so just define the post pre relation'
					]
				)
				'''

				#do the operation
				self.LeakedModelStr+=self.LeakedSymbolStr+"_post"

				#deprefix
				LeakedInteractionWeigthStr=SYS.deprefix(
					self.LeakingWeigthVariable,
					LeakScalarPrefixStr
				)

				#set
				self.LeakedInteractionWeigthFloat=float(LeakedInteractionWeigthStr)

				#add
				self.LeakedModelStr+="="+LeakedInteractionWeigthStr+'*'+self.LeakedVariableStr+"_pre"

			elif self.LeakedClampStr=="Variable":

				#debug
				'''
				self.debug(
					[
						'The interaction is a variable, so define the variable and the post pre relation'
					]
				)
				'''

				#do the operation
				self.LeakedModelStr+=self.LeakedSymbolStr+"_post"

				#add
				self.LeakedModelStr+='='+self.LeakingSymbolPrefixStr+'*'+self.LeakedVariableStr+"_pre"

			#add
			self.LeakedModelStr+=" : "+self.ConnectedToVariable.LeakedDimensionStr

			#debug
			'''
			self.debug(
				[
					'It is a rate interaction so we add the summed term'
				]
			)
			'''

			#Check
			self.LeakedModelStr+=" (summed)"

			#add
			self.LeakedModelStr+="\n"

			#debug
			'''
			self.debug(
				[
					'Ok',
					('self.',self,[
							'LeakedSymbolStr',
							'LeakedModelStr'
						]),
					'We add the interaction in the connected model',
					'self.ConnectedToVariable.LeakedModelStr is ',
					self.ConnectedToVariable.LeakedModelStr,
					'self.ConnectedToVariable.LeakedCurrentStr is ',
					self.ConnectedToVariable.LeakedCurrentStr,
					'self.ConnectedToVariable.LeakedDimensionStr is ',
					self.ConnectedToVariable.LeakedDimensionStr
				]
			)
			'''

			#define in the model
			self.ConnectedToVariable.LeakedModelStr+=self.LeakedSymbolStr+' : '+self.ConnectedToVariable.LeakedDimensionStr+"\n"
			
			#add in the current
			self.ConnectedToVariable.addCurrentStr(self.LeakedSymbolStr)

			#debug
			'''
			self.debug(
				[
					'In the end',
					'self.ConnectedToVariable.LeakedCurrentStr is ',
					self.ConnectedToVariable.LeakedCurrentStr,
					'self.ConnectedToVariable.LeakedModelStr is ',
					self.ConnectedToVariable.LeakedModelStr
				]
			)
			'''

			#/####################/#
			# add delay
			#

			#type
			LeakedDelayType=type(self.LeakingDelayVariable)

			#Check
			if type(self.LeakingDelayVariable)!=None.__class__:

				#debug
				'''
				self.debug(
					[
						'We are going to model delays in the rate',
						('self.',self,[
								'LeakedModelStr'
							]),
						'self.LeakedParentPopulationDeriveLeakerVariable.LeakingTimeVariable is',
						str(self.LeakedParentPopulationDeriveLeakerVariable.LeakingTimeVariable)
					]
				)
				'''
				
				#import
				import numpy as np

				#Check
				if LeakedDelayType in [float,np.float64]:

					#import
					from brian import ms

					#set
					self.LeakedStepTimeFloat=self.LeakedParentNetworkDeriveLeakerVariable.BrianingStepTimeFloat

					#set
					self.LeakedDelayTimeFloat=self.LeakingDelayVariable


				#divide and put that in ms...(rough)
				self.LeakedDelayTimeInt=(int)(
					self.LeakedDelayTimeFloat/
						self.LeakedStepTimeFloat
				)

				#get
				LeakedSymbolStr=self.LeakedParentPopulationDeriveLeakerVariable.LeakedSymbolStr

				#join
				LeakedDefinitionStr="\n".join(
					map(
							lambda __IndexInt:
							LeakedSymbolStr+"_delayer_"+str(
								__IndexInt
							)+" : "+self.LeakedParentPopulationDeriveLeakerVariable.LeakedDimensionStr,
							xrange(self.LeakedDelayTimeInt)
						)
				)

				#add
				self.LeakedModelStr=self.LeakedModelStr.replace(
					LeakedSymbolStr+'_pre',
					LeakedSymbolStr+"_delayer_"+str(self.LeakedDelayTimeInt-1)
				)
				self.LeakedModelStr+=LeakedDefinitionStr

		#debug
		'''
		self.debug(
			[
				'after having setting the delay',
				('self.',self,[
					'LeakedModelStr'
				])	
			]
		)	
		'''

		#/##################/#
		# Look for plasticity in the rate
		#

		#Check
		if self.LeakingPlasticVariable!=None:

			#Check
			if self.LeakingInteractionStr=="Rate":
				
				#debug
				self.debug(
					[
						'It is a rate model',
						('self.',self,[
								'LeakedSymbolStr',
								'LeakingSymbolStr',
								'BrianingSynapsesDict'
							])
					]
				)

				#set
				#BrianedModelStr='beta : 1'
				#BrianedModelStr+='\nlambda : 1'
				#BrianedModelStr+='\nd'+self.LeakingSymbolPrefixStr+'/dt=beta*('
				#BrianedModelStr+='I_Command_post-lambda*'+self.LeakingSymbolPrefixStr+')'	

				#add
				self.LeakedModelStr+="\n"+self.LeakingPlasticVariable

				#debug
				self.debug(
					[
						'after update of the model',
						('self.',self,[
								'LeakedModelStr'
							])
					]
				)

		#/##################/#
		# Update in the Synapses dict
		#

		#Check
		if self.BrianingSynapsesDict==None:
		
			#init
			self.BrianingSynapsesDict={
					'model':self.LeakedModelStr
				}

		else:

			#update
			self.BrianingSynapsesDict['model']=self.LeakedModelStr

		#Check
		if self.LeakingInteractionStr=="Spike":

			#debug
			'''
			self.debug(
				[
					'It is a spike interaction add int the BrianingSynapsesDict pre',
					'self.ConnectedToVariable.LeakedSymbolStr is ',
					self.ConnectedToVariable.LeakedSymbolStr
				]
			)
			'''

			#add
			self.BrianingSynapsesDict['pre']=self.ConnectedToVariable.LeakedSymbolStr+'_post+='+self.LeakingSymbolPrefixStr+'*'+str(
				self.LeakedParentPopulationDeriveLeakerVariable.LeakedQuantityVariable
			)

			#/##################/#
			# Look for plasticity in the spike
			#

			#Check
			if self.LeakingPlasticVariable!=None:

				#debug
				'''
				self.debug(
					[
						'It is a spike model',
						('self.',self,[
								'LeakedSymbolStr'
							])
					]
				)
				'''

				#add
				self.BrianingSynapsesDict['pre']+='\n'+self.LeakingPlasticVariable

				#debug
				'''
				self.debug(
					[
						'after update of the model',
						('self.',self,[
								'BrianingSynapsesDict'
							])
					]
				)
				'''

		#debug
		'''
		self.debug(
			[
				'In the end',
				('self.',self,[
					'BrianingSynapsesDict'
				])
			]
		)
		'''

	def brianPopulation(self):

		#/##################/#
		# link
		#

		#alias
		self.BrianingRecordSkipKeyStrsList=self.LeakedRecordSkipStrsList

		#/##################/#
		# Call the base method
		#

		#debug
		'''
		self.debug(
			[
				'We brianPopulation leak here',
				'We call first the base method',
				('self.',self,[
						'BrianingNeurongroupDict'
					])
			]
		)
		'''

		#call
		BaseClass.brianPopulation(self)

		#/###################/#
		# Set maybe the time constant
		#

		#debug
		'''
		self.debug(
			[
				'Maybe we have to set the time variable'
			]
		)
		'''

		#Check
		if self.LeakedClampStr=="Variable":

			#debug
			'''
			self.debug(
				[
					'We set the time variable',
					('self.',self,[
							'LeakingTimeVariable',
							'LeakedTimeSymbolStr',
							'BrianedTimeQuantityVariable'
						]),
					'getattr(self.BrianedNeurongroupVariable,self.LeakedTimeSymbolStr) is ',
					str(getattr(self.BrianedNeurongroupVariable,self.LeakedTimeSymbolStr))
				]
			)
			'''

			#Check
			if self.LeakingTimeVariable!=0.:

				#set
				getattr(
					self.BrianedNeurongroupVariable,
					self.LeakedTimeSymbolStr
				)[:]=self.LeakingTimeVariable*self.BrianedParentNetworkDeriveBrianerVariable.BrianedTimeQuantityVariable
				
		#debug
		'''
		self.debug(
			[
				'In the end',
				'getattr(self.BrianedNeurongroupVariable,self.LeakedTimeSymbolStr) is ',
				str(getattr(self.BrianedNeurongroupVariable,self.LeakedTimeSymbolStr))
			]
		)
		'''

		#/###################/#
		# Set maybe the threshold
		#

		#Check
		if hasattr(
				self.BrianedNeurongroupVariable,
				'Threshold'
			):

			#debug
			'''
			self.debug(
				[
					'We set the thresholds in the brian Neurongroup',
					('self.',self,[
							'LeakingThresholdVariable',
							'LeakedQuantityVariable'
						])
				]
			)
			'''

			#import 
			import numpy

			#set
			self.BrianedNeurongroupVariable.Threshold[:]=numpy.array(
				self.LeakingThresholdVariable
			)*self.LeakedQuantityVariable

			#debug
			'''
			self.debug(
				[
					'self.BrianedNeurongroupVariable.Threshold is ',
					str(self.BrianedNeurongroupVariable.Threshold)
				]
			)
			'''

			#set in the Threshold Trace to not record
			self.TeamDict[
				'Traces'
			].ManagementDict[
				'*Threshold'
			].BrianingRecordInitBool=False


		#/###################/#
		# Specify a plot of the events
		#

		#Check
		if type(self.LeakingThresholdVariable)!=None.__class__:

			#debug
			'''
			self.debug(
				[
					'We add a record of the events'
				]
			)
			'''

			#get
			self.getTeamer(
					"Events"
				).getManager(
					"Default"
				)





		#/###################/#
		# Reference the transfer function
		#

		#debug
		'''
		self.debug(
			[
				'Maybe we have to refer the transfer function'
			]
		)
		'''

		#Check
		if self.LeakingTransferVariable!=None:

			#Check
			if type(self.LeakingTransferVariable)==str:

				#pass
				pass

			else:

				#
				#self.
				
				#import
				import numpy

				#set
				setattr(
					numpy,
					'F',
					self.LeakingTransferVariable
				)
				#self.F=self.LeakingTransferVariable

				pass

		#/###################/#
		# Special input current case
		#

		#Check
		if 'Inputs' in self.TeamDict:

			#debug
			'''
			self.debug(
				[
					'We are going to set brianInput like in all the input _VariablesList',
				]
			)
			'''

			#map
			map(
				lambda __DeriveLeaker:
				__DeriveLeaker.brianInput(),
				self.TeamDict['Inputs'].ManagementDict.values()
			)


			#/###################/#
			# Resort input traces
			#

			#get
			BrianedTracesManager=self.TeamDict['Traces']

			#debug
			'''
			self.debug(
				[
					'We resort the inputs traces',
					'self.TeamDict["Inputs"].ManagementDict.keys() is ',
					str(self.TeamDict["Inputs"].ManagementDict.keys()),
					'BrianedTracesManager.ManagementDict.keys() is ',
					str(BrianedTracesManager.ManagementDict.keys())

				]	
			)
			'''

			#map
			map(
				lambda __IndexIntAndRecordKeyStr:
				setattr(
					BrianedTracesManager.ManagementDict[
						__IndexIntAndRecordKeyStr[1]
					],
					'GetSortInt',
					__IndexIntAndRecordKeyStr[0]
				) if __IndexIntAndRecordKeyStr[1] in BrianedTracesManager.ManagementDict
				else None,
				enumerate(
					map(
						lambda __DeriveLeaker:
						Recorder.RecordPrefixStr+__DeriveLeaker.LeakedSymbolStr,
						SYS._filter(
							lambda __DeriveLeaker:
							__DeriveLeaker.LeakedClampStr not in ["","Scalar"],
							self.TeamDict['Inputs'].ManagementDict.values()
						)
					)
				)
			)

		"""
		#/################/#
		# Look for computing a global variable
		#

		#Check
		if self.LeakingGlobalBool:

			#debug
			'''
			self.debug(
				[
					'We compute global statistical variables'
				]
			)
			'''

			#import
			from brian2 import Synapses,StateMonitor

			#set
			LeakedMeanGlobalSymbolStr='Mean_'+self.LeakedSymbolStr
			LeakedVarGlobalSymbolStr='Var_'+self.LeakedSymbolStr

			#set
			LeakedGlobalModelStr=LeakedMeanGlobalSymbolStr+'_post = '+self.LeakedSymbolStr+'_pre/'+str(
				self.LeakingUnitsInt
			)+' : '+self.LeakedDimensionStr+' (summed)\n'

			#set
			LeakedGlobalModelStr+=LeakedVarGlobalSymbolStr+'_post = (1/'+self.LeakedDimensionStr+')*(('+self.LeakedSymbolStr+'_pre-'+LeakedMeanGlobalSymbolStr+'_pre)**2)/'+str(
				self.LeakingUnitsInt-1
			)+' : 1 (summed)\n'

			#debug
			self.debug(
				[
					'LeakedGlobalModelStr is ',
					LeakedGlobalModelStr
				]
			)

			#init
			self.LeakedGlobalSynapsesVariable=Synapses(
				self.BrianedNeurongroupVariable,
				self.BrianedNeurongroupVariable,
				LeakedGlobalModelStr,
				clock=self.BrianedNeurongroupVariable.clock
			)
			self.LeakedGlobalSynapsesVariable.connect(True)

			#init
			self.LeakedMeanStateMonitorVariable=StateMonitor(
				self.LeakedGlobalSynapsesVariable,
				LeakedMeanGlobalSymbolStr,
				[0]
			)

			#init
			self.LeakedVarStateMonitorVariable=StateMonitor(
				self.LeakedGlobalSynapsesVariable,
				LeakedVarGlobalSymbolStr,
				[0]
			)

			#debug
			'''
			self.debug(
				[
					'self.BrianedNeurongroupVariable.N is ',
					str(self.BrianedNeurongroupVariable.N),
					('self.',self,[
						'LeakedGlobalSynapsesVariable',
						'LeakedMeanStateMonitorVariable'
					])
				]
			)
			'''

			#add
			self.BrianedParentNetworkDeriveBrianerVariable.BrianedNetworkVariable.add(
				self.LeakedGlobalSynapsesVariable
			)
			self.BrianedParentNetworkDeriveBrianerVariable.BrianedNetworkVariable.add(
				self.LeakedMeanStateMonitorVariable
			)
			self.BrianedParentNetworkDeriveBrianerVariable.BrianedNetworkVariable.add(
				self.LeakedVarStateMonitorVariable
			)
		"""

	def brianInput(self):

		#debug
		'''
		self.debug(
			[
				'We set input brian here',
			]
		)	
		'''

		#Check
		if self.LeakingWeigthVariable!=None:

			#Check
			if self.LeakedClampStr=="Variable":

				#get
				Variable=getattr(
					self.LeakedParentPopulationDeriveLeakerVariable.BrianedNeurongroupVariable,
					self.LeakedSymbolStr
				)

				#debug
				'''
				self.debug(
					[
						'This input is just a constant value'
					]
				)
				'''

				#set
				setattr(
					self.LeakedParentPopulationDeriveLeakerVariable.BrianedNeurongroupVariable,
					self.LeakedSymbolStr,
					self.LeakingWeigthVariable*Variable.unit
				)

			elif self.LeakedClampStr=='Equation':

				#debug
				'''
				self.debug(
					[
						'This input is time varying and it is an equation',
						('self.',self,[
							'LeakedSymbolStr'
						])
					]
				)
				'''

			elif self.LeakedClampStr=='TimedArray':

				#import
				from brian2 import TimedArray

				#init
				self.LeakedTimedArrayVariable=TimedArray(
					self.LeakingWeigthVariable,
					dt=self.LeakedParentPopulationDeriveLeakerVariable.BrianedNeurongroupVariable.clock.dt
				)

				#import sys
				#set in the population
				'''
				setattr(
					#self.LeakedParentPopulationDeriveLeakerVariable,
					#sys.modules['__main__'],
					self.LeakedParentPopulationDeriveLeakerVariable.BrianedNeurongroupVariable,
					self.LeakedSymbolStr,
					self.LeakedTimedArrayVariable
				)
				#globals()[self.LeakedSymbolStr]=self.LeakedTimedArrayVariable
				'''
				setattr(
					self.LeakedParentPopulationDeriveLeakerVariable.BrianedNeurongroupVariable,
					self.LeakedSymbolStr,
					self.LeakedTimedArrayVariable
				)

			elif self.LeakedClampStr=='Custom':

				#debug
				'''
				self.debug(
					[
						'We are going to do a custom operation',
						('self.',self,[
							'LeakedEquationStr',
							'LeakedSymbolStr'
						])
					]
				)
				'''

				#Check
				if '#SymbolStr' in self.LeakedEquationStr:

					#replace
					LeakedEquationStr=self.LeakedEquationStr.replace(
						'#SymbolStr',
						self.LeakedSymbolStr
					)
				else:

					#set
					LeakedEquationStr=self.LeakedSymbolStr+"="+self.LeakedEquationStr

				#debug
				'''
				self.debug(
					[
						'In the end',
						('self.',self,[
							'LeakedEquationStr',
							'LeakedClockStr'
						]),
						'LeakedEquationStr is '+LeakedEquationStr
					]
				)
				'''

				#Check
				if self.LeakedClockStr=="":

					#custom
					LeakedCustomoperation=self.LeakedParentPopulationDeriveLeakerVariable.BrianedNeurongroupVariable.custom_operation(
						LeakedEquationStr
					)

				else:

					#split
					LeakedStrsList=self.LeakedClockStr.split('*')

					#import
					import brian2

					#debug
					'''
					self.debug(
						[
							'LeakedStrsList is '+str(LeakedStrsList)
						]
					)
					'''

					#custom
					LeakedCustomoperation=self.LeakedParentPopulationDeriveLeakerVariable.BrianedNeurongroupVariable.custom_operation(
						LeakedEquationStr,
						dt=int(LeakedStrsList[0])*getattr(
							brian2,
							LeakedStrsList[1]
						)
					)

				#add
				self.LeakedParentNetworkDeriveLeakerVariable.BrianedNetworkVariable.add(
					LeakedCustomoperation
				)

				#debug
				'''
				self.debug(
					[
						'In the end',
						'self.LeakedParentPopulationDeriveLeakerVariable.BrianedNeurongroupVariable is ',
						str(self.LeakedParentPopulationDeriveLeakerVariable.BrianedNeurongroupVariable)
					]
				)
				'''

			elif self.LeakedClampStr=='Network':

				#debug
				'''
				self.debug(
					[
						'We are going to do a network operation',
						('self.',self,[
							'LeakedEquationStr',
							'LeakedSymbolStr'
						])
					]
				)
				'''

				#import
				from brian2 import network_operation

				#alias
				BrianedNeurongroupVariable=self.LeakedParentPopulationDeriveLeakerVariable.BrianedNeurongroupVariable

				BrianedInputQuantity=getattr(
						BrianedNeurongroupVariable,
						self.LeakedSymbolStr
					)

				if self.LeakedClockStr=="":

					@network_operation
					def updateInput():

						#get set
						BrianedInputQuantity[:]=self.LeakingWeigthVariable[1](
							BrianedInputQuantity,
							BrianedNeurongroupVariable.clock.t
						)

				else:

					#split
					LeakedStrsList=self.LeakedClockStr.split('*')

					#import
					import brian2

					#debug
					'''
					self.debug(
						[
							'LeakedStrsList is '+str(LeakedStrsList)
						]
					)
					'''

					@network_operation(
						dt=int(LeakedStrsList[0])*getattr(
							brian2,
							LeakedStrsList[1]
						)
					)
					def updateInput():

						#get set
						BrianedInputQuantity[:]=self.LeakingWeigthVariable[1](
							BrianedInputQuantity,
							BrianedNeurongroupVariable.clock.t
						)

				#add
				self.LeakedParentNetworkDeriveLeakerVariable.BrianedNetworkVariable.add(
					updateInput
				)
	
	def brianInteraction(self):

		#/##################/#
		# Call the base method
		#

		#debug
		'''
		self.debug(
			[
				'We brianInteraction leak here',
				'We call first the base method',
				('self.',self,[
						'LeakingWeigthVariable'
					])
			]
		)
		'''

		#call
		BaseClass.brianInteraction(self)

		#Check
		if self.BrianedSynapsesVariable==None:
			return

		#/###############/#
		# Determine the good row and col ints
		#

		#get
		BrianedRowsInt=self.BrianedSynapsesVariable.source.N
		BrianedColsInt=self.BrianedSynapsesVariable.target.N

		#/##################/#
		# Maybe we specify the connection
		#

		#debug
		'''
		self.debug(
			[
				'We set interaction brian here',
				('self.',self,[
						'LeakedClampStr'
					])
			]
		)
		'''

		#Check
		if self.LeakedClampStr=="Scalar":

			#debug
			'''
			self.debug(
				[
					'Look for a non nul connection',
					('self.',self,['LeakedInteractionWeigthFloat'])
				]
			)
			'''

			#Check
			if self.LeakedInteractionWeigthFloat!=0.:

				#debug
				'''
				self.debug(
					[
						'It is a non nul constant connection',
						'we connect True'
					]
				)
				'''

				#connect
				self.BrianedSynapsesVariable.connect(
					True
				)

		elif self.LeakedClampStr=="Variable":

			#type
			BrianedInteractionType=type(self.LeakingWeigthVariable)

			#debug
			'''
			self.debug(
				[
					'We have to set the connect variable',
					('self.',self,[
						'LeakingWeigthVariable'
					]),
					'BrianedInteractionType is ',
					str(BrianedInteractionType)
				]
			)
			'''

			#import
			import numpy as np

			#Check
			if BrianedInteractionType in [float,np.float64]:

				#debug
				'''
				self.debug(
					[
						'It is just one value',
						'We set in the synapses if it is not null',
						('self.',self,[
								'LeakingWeigthVariable'
							])
					]
				)
				'''

				#Check
				if self.LeakingWeigthVariable!=0.:

					#debug
					'''
					self.debug(
						[
							'We are going to connect this Variable for each index',
							('self.',self,[
									'LeakingWeigthVariable'
								])
						]
					)
					'''

					#connect
					self.BrianedSynapsesVariable.connect(
						True
					)

					#get and set
					getattr(
						self.BrianedSynapsesVariable,
						self.LeakingSymbolPrefixStr
					)[:]=self.LeakingWeigthVariable
					

				#debug
				'''
				self.debug(
					[
						'In the end ',
						'getattr(self.BrianedSynapsesVariable,self.LeakingSymbolPrefixStr) is ',
						str(getattr(self.BrianedSynapsesVariable,self.LeakingSymbolPrefixStr))
					]
				)
				'''

			else:

				#/###############/#
				# Build or not the matrix array
				#

				#Check
				if BrianedInteractionType not in [list,tuple,np.ndarray]:

					#debug
					'''
					self.debug(
						[
							'It is an array that we have to build before'
						]
					)
					'''

					#numscipy
					self.NumscipyingRowsInt=BrianedRowsInt
					self.NumscipyingColsInt=BrianedColsInt
					self.numscipy()

					#alias
					BrianedWeigthFloatsArray=self.NumscipiedRandomFloatsArray

				else:

					#shape
					BrianedWeigthFloatsArray=getShapeArray(
						self.LeakingWeigthVariable,
						BrianedRowsInt,
						BrianedColsInt
					)

				#/###############/#
				# Shape correctly
				#

				#reshape
				BrianedFloatsArray=np.reshape(
					np.array(
						BrianedWeigthFloatsArray
					).T,
					BrianedRowsInt*BrianedColsInt
				)

				#debug
				'''
				self.debug(
					[
						'It is an already defined array',
						('self.',self,[
								'LeakingWeigthVariable'
							]),
						'self.BrianedSynapsesVariable.source.N is '+str(self.BrianedSynapsesVariable.source.N),
						'self.BrianedSynapsesVariable.target.N is '+str(self.BrianedSynapsesVariable.target.N),
						'BrianedFloatsArray is '+str(BrianedFloatsArray)
					]
				)
				'''
				
				#connect
				self.BrianedSynapsesVariable.connect(
					True
				)

				#get
				BrianedInteractionArray=getattr(
					self.BrianedSynapsesVariable,
					self.LeakingSymbolPrefixStr
				)

				#get and set
				BrianedInteractionArray[:]=BrianedFloatsArray

				#debug
				'''
				self.debug(
					[
						'In the end ',
						'BrianedInteractionArray is ',
						str(BrianedInteractionArray)
					]
				)
				'''

		#/##################/#
		# Look for delay
		#

		#type
		LeakedDelayType=type(self.LeakingDelayVariable)

		#Check
		if LeakedDelayType!=None.__class__:

			#debug
			'''
			self.debug(
				[
					'We are going to add delay',
					('self.',self,[
							'LeakingDelayVariable'
						])
				]
			)
			'''

			#Check
			if self.LeakingInteractionStr=="Spike":

				#Check
				if LeakedDelayType in [float,np.float64]:

					#debug
					'''
					self.debug(
						[
							'We set the float delay',
							'self.BrianedSynapsesVariable.pre.delay is ',
							str(self.BrianedSynapsesVariable.pre.delay)
						]
					)
					'''

					#set
					self.BrianedSynapsesVariable.pre.delay=self.LeakingDelayVariable*self.LeakedParentNetworkDeriveLeakerVariable.BrianedTimeQuantityVariable

					#debug
					'''
					self.debug(
						[
							'We set the float delay',
							'self.BrianedSynapsesVariable.pre.delay is ',
							str(self.BrianedSynapsesVariable.pre.delay)
						]
					)
					'''

				elif LeakedDelayType in [np.ndarray,list]:

					#debug
					'''
					self.debug(
						[
							'We set the array delay',
							'self.BrianedSynapsesVariable.pre.delay is ',
							str(self.BrianedSynapsesVariable.pre.delay),

						]
					)
					'''

					#shape
					BrianedDelayFloatsArray=getShapeArray(
						self.LeakingDelayVariable,
						BrianedRowsInt,
						BrianedColsInt
					)

					#reshape
					BrianedDelayFloatsArray=np.reshape(
						np.array(
							BrianedDelayFloatsArray
						).T,
						BrianedRowsInt*BrianedColsInt
					)

					#set
					self.BrianedSynapsesVariable.pre.delay[:
					]=BrianedDelayFloatsArray*self.LeakedParentNetworkDeriveLeakerVariable.BrianedTimeQuantityVariable

					#debug
					'''
					self.debug(
						[
							'We set the array delay',
							'self.BrianedSynapsesVariable.pre.delay is ',
							str(self.BrianedSynapsesVariable.pre.delay),
							'BrianedDelayFloatsArray is ',
							str(BrianedDelayFloatsArray)
						]
					)
					'''

			else:

				#debug
				self.debug(
					[
						'This is a rate model',
						'add the delay as a custom operation',
						('self.',self,[
								'LeakedDelayTimeInt'
							])
					]
				)

				#alias
				LeakedSymbolStr=self.LeakedParentPopulationDeriveLeakerVariable.LeakedSymbolStr

				#join
				BrianedDelayStr='\n'.join(
					map(
							lambda __IndexInt:
							LeakedSymbolStr+"_delayer_"+str(
								__IndexInt
							)+"="+LeakedSymbolStr+"_delayer_"+str(
								__IndexInt-1
							),
							xrange(self.LeakedDelayTimeInt-1,0,-1)
						)+[
						LeakedSymbolStr+"_delayer_0="+LeakedSymbolStr+'_pre'
					]
				)
				
				#debug
				self.debug(
					[
						'BrianedDelayStr is '+str(BrianedDelayStr)
					]
				)

				#custom
				self.LeakedParentNetworkDeriveLeakerVariable.BrianedNetworkVariable.add(
					self.BrianedSynapsesVariable.custom_operation(
						BrianedDelayStr,
						dt=self.BrianedSynapsesVariable.clock.dt
					)
				)

	def brianTrace(self):

		#/##################/#
		# Check for non recorded variables 
		# 
		
		#debug
		'''
		self.debug(
			[
				'We are in brian trace',
				'Check if it is not the trace of the variable time constant',
				('self.',self,[
					'ManagementTagStr',
				]),
				'self.LeakedParentPopulationDeriveLeakerVariable.LeakedRecordSkipStrsList is ',
				self.LeakedParentPopulationDeriveLeakerVariable.LeakedRecordSkipStrsList,
				'self.LeakedParentPopulationDeriveLeakerVariable.LeakingTimeVariable is ',
				str(self.LeakedParentPopulationDeriveLeakerVariable.LeakingTimeVariable)
			]
		)
		'''

		#Check
		if self.ManagementTagStr.split(
			Recorder.RecordPrefixStr
		)[1] in self.LeakedParentPopulationDeriveLeakerVariable.LeakedRecordSkipStrsList or (
			self.LeakedParentPopulationDeriveLeakerVariable.LeakingTimeVariable in ['0',0.]
		):

			#debug
			'''
			self.debug(
				[
					'We are not recording init this variable'
				]
			)
			'''

			#set to false
			self.BrianingRecordInitBool=False

		#/##################/#
		# Check also for the interaction case
		#

		#reget...
		BrianedParentInteractionDeriveBrianerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

		#Check
		if BrianedParentInteractionDeriveBrianerVariable.BrianedSynapsesVariable!=None:

			#Check
			if BrianedParentInteractionDeriveBrianerVariable.LeakingPlasticVariable!=None and BrianedParentInteractionDeriveBrianerVariable.LeakingWeigthVariable!=None:

				#debug
				'''
				self.debug(
					[
						'This is plastic with some initial conditions'
					]
				)
				'''

				#set to false
				self.BrianingRecordInitBool=False

		#/##################/#
		# Call the base method
		#

		#call
		BaseClass.brianTrace(self)

		#debug
		'''
		self.debug(
			[
				'We are going to  brian leak a Trace'
			]
		)
		'''

		#/##################/#
		# Check the variable that has a threshold
		#

		#Check
		if hasattr(
			self.LeakedParentPopulationDeriveLeakerVariable.BrianedNeurongroupVariable,
			'Threshold'
		):

			#Check
			if self.RecordKeyStr==self.LeakedParentPopulationDeriveLeakerVariable.LeakedSymbolStr:

				#min value
				self.LeakedMinFloat=self.RecordedInitFloatsArray.min()
				self.LeakedMinFloat=self.LeakedMaxFloat-0.1*self.LeakedMaxFloat

				#debug
				'''
				self.debug(
					[
						'We init under the thresholds',
						('self.',self,[
								'ManagementTagStr',
								'RecordKeyStr',
								'RecordedInitFloatsArray',
								'LeakedMaxFloat',
								'LeakedMinFloat'
							])
					]
				)
				'''

				#type
				LeakedThresholdType=type(self.LeakedParentPopulationDeriveLeakerVariable.LeakingThresholdVariable)

				#map
				map(
					lambda __IndexInt:
					self.RecordedInitFloatsArray.__setitem__(
						__IndexInt,
						self.LeakedMinFloat
					)
					if self.RecordedInitFloatsArray[__IndexInt]>self.LeakedMaxFloat
					else None,
					xrange(len(self.RecordedInitFloatsArray))
				)

				#debug
				'''
				self.debug(
					[
						'In the end ',
						('self.',self,[
								'RecordedInitFloatsArray'
							])
					]
				)
				'''

		#/##################/#
		# Case of an input variable
		#

		BrianedInputStr=SYS.deprefix(
			self.ManagementTagStr,
			Recorder.RecordPrefixStr
		)

		#Check
		if BrianedInputStr.startswith(
			LeakInputPrefixStr
		):

			#join
			BrianedManagementStr='_'.join(BrianedInputStr.split('_')[1:])

			#debug
			'''
			self.debug(
				[
					'It is an input trace',
					'BrianedManagementStr is '+str(BrianedManagementStr),
				]
			)
			'''

			#get
			BrianedInputDeriveLeaker=self.LeakedParentPopulationDeriveLeakerVariable.TeamDict[
				'Inputs'
			].ManagementDict[
				BrianedManagementStr
			]

			#debug
			'''
			self.debug(
				[
					'BrianedInputDeriveLeaker.LeakedClampStr is '+BrianedInputDeriveLeaker.LeakedClampStr,
					'BrianedInputDeriveLeaker.LeakedOperationStr is '+BrianedInputDeriveLeaker.LeakedOperationStr
				]
			)
			'''

			#Check
			if BrianedInputDeriveLeaker.LeakedClampStr not in ["Scalar","Variable"]:

				#debug
				'''
				self.debug(
					[
						'It is not a scalar neither a variable so we have to plot it'
					]
				)
				'''

				#manage
				BrianedDefaultDeriveLeaker=self.TeamDict['Samples'].manage(
					'Default'
				).ManagedValueVariable

				#Check
				if BrianedDefaultDeriveLeaker.RecordingLabelVariable==None:

					#debug
					'''
					self.debug(
						[
							'This input has no special recording label variable so take the one of the parent population'
						]
					)	
					'''

					#Check
					if self.LeakedParentPopulationDeriveLeakerVariable.BrianedNeurongroupVariable.N>len(
							self.LeakedParentPopulationDeriveLeakerVariable.LeakingMonitorIndexIntsList
						):

						#alias
						BrianedDefaultDeriveLeaker.RecordingLabelVariable=self.LeakedParentPopulationDeriveLeakerVariable.LeakingMonitorIndexIntsList

					else:

						#debug
						'''
						self.debug(
							[
								'WARNING : size is not good',
								'self.LeakedParentPopulationDeriveLeakerVariable.BrianedNeurongroupVariable.N is',
								str(self.LeakedParentPopulationDeriveLeakerVariable.BrianedNeurongroupVariable.N),
								'self.LeakedParentPopulationDeriveLeakerVariable.LeakingMonitorIndexIntsList is ',
								str(self.LeakedParentPopulationDeriveLeakerVariable.LeakingMonitorIndexIntsList)
							]
						)
						'''
						
						#alias
						BrianedDefaultDeriveLeaker.RecordingLabelVariable=[0]

	def mimic__print(self,**_KwargVariablesDict):

		#/##################/#
		# Modify the printing Variable
		#

		#Check
		if self.PrintingSelfBool:

			#/##################/#
			# Print the leaked Model str if it is defined
			#

			#Check
			if self.LeakedModelStr!='':

				#Check
				if 'PrintDeepInt' in _KwargVariablesDict:
					PrintedDeepInt=_KwargVariablesDict['PrintDeepInt']
				else:
					PrintedDeepInt=0

				#join
				PrintedAlineaStr="".join([Printer.PrintIndentStr]*(PrintedDeepInt+3))

				#debug
				'''
				print('Leaker l 409')
				print('PrintedDeepInt is ')
				print(PrintedDeepInt)
				print('PrintedAlineaStr is ')
				print(PrintedAlineaStr)
				print('')
				'''

				#replace
				self.PrintingCopyVariable.LeakedModelStr=self.LeakedModelStr.replace(
					'\n','\n'+PrintedAlineaStr
				)

				#add
				self.forcePrint(
					['LeakedModelStr'],
					'LeakerClass'
				)

		#/##################/#
		# Call the base method
		#

		#call
		BaseClass._print(self,**_KwargVariablesDict)
		
	def addCurrentStr(self,_CurrentStr):

		#debug
		'''
		self.debug(
			[
				'We add current here',
				('self.',self,[
					'LeakedCurrentStr'
				]),
				'_CurrentStr is '+_CurrentStr
			]
		)
		'''

		#Check
		if self.LeakedCurrentStr=="":
			self.LeakedCurrentStr=_CurrentStr
		else:
			self.LeakedCurrentStr+='+'+_CurrentStr

	def filterLeak(self):

		#/#################/#
		# Look for the StructureTopDeriveStructurerRigidVariable
		#

		#debug
		'''
		self.debug(
			[
				'Check if we can leak',
				'self.StructureTopDeriveStructurerRigidVariable!=None',
				str(self.StructureTopDeriveStructurerRigidVariable!=None)
			]
		)
		'''

		#Check
		if self.StructureTopDeriveStructurerRigidVariable!=None:

			#Check
			if self.StructureTopDeriveStructurerRigidVariable.StructureFilterTeamTagStrsList!=None:

				#Check
				if self.ParentDeriveTeamerVariable!=None:

					#debug
					'''
					self.debug(
						[
							'Check if we can leak',
							'self.ParentDeriveTeamerVariable.TeamTagStr is ',
							str(self.ParentDeriveTeamerVariable.TeamTagStr)
						]
					)
					'''
					
					#Check
					if self.ParentDeriveTeamerVariable.TeamTagStr in self.StructureTopDeriveStructurerRigidVariable.StructureFilterTeamTagStrsList:

						#return
						return

		#leak
		self.leak()

	def setDimension(self):

		#import 
		import brian2

		#get
		self.LeakedQuantityVariable=getattr(
			brian2,
			self.LeakingQuantityStr
		)

		#repr
		LeakedQuantityReprStr=repr(self.LeakedQuantityVariable)

		#loop
		for __DimensionStr in ['volt']:

			#Check
			if LeakedQuantityReprStr.endswith(__DimensionStr):
				
				#set
				self.LeakedDimensionStr=__DimensionStr

				#return
				return

		#str
		self.LeakedDimensionStr=repr(
			self.LeakedQuantityVariable.dim
		)

	def setOperation(self):

		#debug
		'''
		self.debug(
			[
				'We set the operation',
				"self.LeakedParentPopulationDeriveLeakerVariable.LeakedModelStr is ",
				self.LeakedParentPopulationDeriveLeakerVariable.LeakedModelStr,
				('self.',self,[
					'LeakedOperationStr'
				])
			]
		)
		'''

		#Check
		if LeakClockPrefixStr in self.LeakedOperationStr:

			#split
			LeakedStrsList=self.LeakedOperationStr.split(':')

			#debug
			'''
			self.debug(
				[
					'There is a specification of the clock',
					'LeakedStrsList is '+str(LeakedStrsList)
				]
			)
			'''

			#deprefix
			self.LeakedClockStr=LeakedStrsList[1]

			#Check
			if self.LeakedClampStr!='Network':

				#join
				self.LeakedEquationStr=':'.join(
					LeakedStrsList[2:]
				)

		else:

			#Check
			if self.LeakedClampStr!='Network':

				#set direct
				self.LeakedEquationStr=self.LeakedOperationStr

		#debug
		'''
		self.debug(
			[
				(
					'self.',self,[
						'LeakedSymbolStr',
						'LeakedClockStr',
						'LeakedEquationStr'
					]
				)
			]
		)
		'''

		#Check
		if self.LeakedParentPopulationDeriveLeakerVariable.LeakedQuantityVariable==None:
			self.LeakedParentPopulationDeriveLeakerVariable.setDimension()

		#define in the model
		if self.LeakedClampStr=='Equation':
			self.LeakedParentPopulationDeriveLeakerVariable.LeakedModelStr+=self.LeakedSymbolStr+'='+self.LeakedEquationStr+' : '+self.LeakedParentPopulationDeriveLeakerVariable.LeakedDimensionStr+"\n"
		elif self.LeakedClampStr in ['Custom','Network']:
			self.LeakedParentPopulationDeriveLeakerVariable.LeakedModelStr+=self.LeakedSymbolStr+' : '+self.LeakedParentPopulationDeriveLeakerVariable.LeakedDimensionStr+"\n"

		#add in the current
		self.LeakedParentPopulationDeriveLeakerVariable.addCurrentStr(
			self.LeakedSymbolStr
		)

	def viewPopulation(self):

		#base
		BaseClass.viewPopulation(self)

		#debug
		'''
		self.debug(
			[
				'We view leak pop here',
				('self.',self,[
						'BrianingViewNetworkBool'
					])
			]
		)
		'''

		#Check
		if self.BrianingViewNetworkBool:

			#Check
			if self.LeakedMeanStateMonitorVariable!=None:

				#debug
				'''
				self.debug(
					[
						'We add the global variable to the view',
						('self.',self,[
								'LeakedSymbolStr'
							])
					]
				)
				'''

				#import
				import brian2

				#get
				ViewedMonitorVariable=getattr(
										self.LeakedMeanStateMonitorVariable,
										'Mean_'+self.LeakedSymbolStr
									)

				#get 
				ViewedMeanFloatsArray=getattr(
										self.LeakedMeanStateMonitorVariable,
										'Mean_'+self.LeakedSymbolStr
									)[0,:]/getattr(
										self.BrianedNeurongroupVariable,
										'Mean_'+self.LeakedSymbolStr
									).unit

				#import
				import numpy as np

				#get
				ViewedStdFloatsArray=np.sqrt(
					getattr(
										self.LeakedVarStateMonitorVariable,
										'Var_'+self.LeakedSymbolStr
									)[0,:]
				)

				#debug
				self.debug(
					[
						'ViewedMeanFloatsArray is ',
						str(ViewedMeanFloatsArray),
						'ViewedStdFloatsArray is ',
						str(ViewedStdFloatsArray)
					]
				)

				#add
				self.getTeamer(
						'Charts'
					).getManager(
						Recorder.RecordPrefixStr+self.LeakedSymbolStr
					).getTeamer(
						'Draws'
					).getManager(
						'Global'
					).PyplotingDrawVariable=[
						(	
							'plot',
							{
								'#liarg':[
									self.LeakedMeanStateMonitorVariable.t,
									ViewedMeanFloatsArray
								],
								'#kwarg':dict(
									{
										'linestyle':'-',
										'linewidth':3,
										'color':'black',
										#'label':'$<'+self.LeakedSymbolStr+'>$'
										'label':'$mean('+self.LeakedSymbolStr+')$'
									}
								)
							}	
						),
						(	
							'plot',
							{
								'#liarg':[
									self.LeakedMeanStateMonitorVariable.t,
									ViewedMeanFloatsArray+(ViewedStdFloatsArray/2.)
								],
								'#kwarg':dict(
									{
										'linestyle':'--',
										'linewidth':1,
										'color':'black',
										#'label':'$<('+self.LeakedSymbolStr+'-<'+self.LeakedSymbolStr+'>)^2>$'
										'label':'$std('+self.LeakedSymbolStr+')$'
									}
								)
							}	
						),
						(	
							'plot',
							{
								'#liarg':[
									self.LeakedMeanStateMonitorVariable.t,
									ViewedMeanFloatsArray-(ViewedStdFloatsArray/2.)
								],
								'#kwarg':dict(
									{
										'linestyle':'--',
										'linewidth':1,
										'color':'black',
									}
								)
							}	
						)
					]

	def mimic_simulate(self):

		#/########################/#
		# Network level
		# 

		#Check
		if (self.ParentDeriveTeamerVariable==None or 'Populations' in self.TeamDict or self.ParentDeriveTeamerVariable.TeamTagStr not in [
			'Clocks',
			'Traces',
			'Samples',
			'Events',
			'Interactomes',
			'Interactions'
		]) and self.BrianedParentSingularStr!='Population':

			#debug
			'''
			self.debug(
				[
					'It is a Network level',
					'We sructure simulate'
				]
			)
			'''

			#/########################/#
			# Special Network level
			# 

			#Check
			if 'Populations' not in self.TeamDict:
		
				#debug
				'''
				self.debug(
					[
						'It is a network with a one level pop',
						'So simulatePopulation'
					]
				)
				'''

				#simulatePopulation
				self.simulatePopulation()

				#debug
				'''
				self.debug(
					[
						'We end to simulatePopulation for this network'
					]
				)
				'''


			#/########################/#
			# simulate first
			#	

			#self
			BaseClass.simulate(self)

			#/########################/#
			# structure
			# 

			#debug
			'''
			self.debug(
				[
					'We view structure in all the brian children...',
				]
			)
			'''

			#structure
			self.structure(
				[
					'Clocks',
					'Populations',
					'Traces',
					'Events',
					'Samples',
					'Interactomes',
					'Interactions'
				],
				'#all',
				_ManagerCommandSetList=[
					'simulate'
				]
			)

			#debug
			'''
			self.debug(
				[
					'Ok we have simulate structured all the brian children...',
				]
			)	
			'''

		elif self.BrianedParentSingularStr!="":

			#set
			BrianedMethodKeyStr='simulate'+self.BrianedParentSingularStr

			#debug
			'''
			self.debug(
				[
					'Ok we check if this parentsingular has a special method ',
					('self.',self,[
						'BrianedParentSingularStr'
					])
				]
			)
			'''

			#Check
			if hasattr(self,BrianedMethodKeyStr):

				#/########################/#
				# call the special view<BrianedParentSingularStr> method
				#

				#debug
				'''
				self.debug(
					[
						'It is a '+self.BrianedParentSingularStr+' level',
						'We view<BrianedParentSingularStr>'
					]
				)
				'''

				#call
				getattr(
					self,
					BrianedMethodKeyStr
				)()

				#debug
				'''
				self.debug(
					[
						'Ok we have setted simulate'+self.BrianedParentSingularStr
					]
				)
				'''	

		#debug
		'''
		self.debug(
			[
				'End of mimic_simulate'
			]
		)
		'''

	def simulatePopulation(self):

		#debug
		self.debug(
			[
				'We simulate population here'
			]
		)

		#Check
		if self.LeakingGlobalBool:

			SimulatedFloatsArray=getattr(
				self.BrianedNeurongroupVariable
				self.LeakedSymbolStr
			)

			self.LeakedMeanFloatsArray=


#</DefineClass>

#<DefineLocals>

#map
map(
	lambda __ItemTuple:
	map(
		lambda __Class:
		setattr(
			__Class,
			__ItemTuple[0],__ItemTuple[1]
		) if hasattr(__Class,__ItemTuple[0])
		else None,
		LeakerClass.__mro__
	),
	dict(
		{
			'PyplotingPrintBool':False,
			'BrianingPrintBool':False
		}
	).items()
)

#</DefineLocals>

#</DefinePrint>
LeakerClass.PrintingClassSkipKeyStrsList.extend(
	[
		'LeakingUnitsInt',
		'LeakingSymbolStr',
		'LeakingTimeVariable',
		'LeakingQuantityStr',
		'LeakingMonitorIndexIntsList',
		'LeakingTimeUnitStr',
		'LeakingInteractionStr',
		'LeakingSymbolPrefixStr',
		'LeakingWeigthVariable',
		'LeakingTransferVariable',
		'LeakingThresholdVariable',
		'LeakingResetVariable',
		'LeakingVariableStr',
		'LeakingRecordBool',
		'LeakingNoiseStdVariable',
		'LeakingDelayVariable',
		'LeakingPlasticVariable',
		'LeakingGlobalBool',
		'LeakedRecordSkipStrsList',
		'LeakedQuantityVariable',
		'LeakedDimensionStr',
		'LeakedClampStr',
		'LeakedSymbolStr',
		'LeakedOperationStr',
		'LeakedEquationStr',
		'LeakedClockStr',
		'LeakedModelStr',
		'LeakedCurrentStr',
		'LeakedTimeSymbolStr',
		'LeakedInteractionWeigthFloat',
		'LeakedParentSingularStr',
		'LeakedParentNetworkDeriveLeakerVariable',
		'LeakedParentPopulationDeriveLeakerVariable',
		'LeakedParentInteractomeDeriveLeakerVariable',
		'LeakedTimedArrayVariable',
		'LeakedVariableStr',
		'LeakedDelayTimeFloat',
		'LeakedDelayTimeInt',
		'LeakedMinFloat',
		'LeakedMaxFloat',
		#'LeakedGlobalSynapsesVariable',
		#'LeakedMeanStateMonitorVariable',
		#'LeakedVarStateMonitorVariable'
		'LeakedMeanFloatsArray',
		'LeakedStdFloatsArray'
	]
)
#<DefinePrint>
