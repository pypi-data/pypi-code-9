# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


A Brianer

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Recorders.Simulater"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
from ShareYourSystem.Standards.Interfacers import Printer
from ShareYourSystem.Standards.Recorders import Recorder
#</ImportSpecificModules>

#<DefineLocals>
BrianViewKeyStrsList=[
				'ViewingXLabelStr',
				'ViewingYLabelStr',
				'ViewingXVariable',
				'ViewingYVariable',
				'ViewingAddXMinFloat',
				'ViewingAddXMaxFloat',
				'ViewingAddYMinFloat',
				'ViewingAddYMaxFloat',
				'ViewingXScaleFloat',
				'ViewingYScaleFloat',
				'ViewingXIndexBool',
				'ViewingYIndexBool',
				'ViewingXSampleInt',
				'ViewingYSampleInt'
			]
#</DefineLocals>

#<DefineClass>
@DecorationClass(**{
	'ClassingSwitchMethodStrsList':['brian'],
	'ClassingStructureVariable':[
			('Clock','Clocks'),
			("Population",'Populations'),
			('Trace','Traces'),
			('Sample','Samples'),
			('Event','Events'),
			('Rate','Rates'),
			('Interactome','Interactomes'),
			('Interaction','Interactions')
		]
})
class BrianerClass(BaseClass):
		
	def default_init(self,
			_BrianDebugTimeFloat={
				'DefaultValueType':property,
				'PropertyInitVariable':0.,
				'PropertyDocStr':'I am displaying bug'
			},
			_BrianingNeurongroupDict=None,
			_BrianingSynapsesDict=None,
			_BrianingConnectVariable=None,
			_BrianingTraceDict=None,
			_BrianingMoniterTuple=None,
			_BrianingSpikesDict=None,
			_BrianingPyplotDict=None,
			_BrianingTimeQuantityStr='ms',
			_BrianingActivityQuantityStr='mV',
			_BrianingPyplotBool=True,
			_BrianingStepTimeFloat=0.1,
			_BrianingDebugVariable=0,
			_BrianingRecordInitBool=True,
			_BrianingRecordSkipKeyStrsList=None,
			_BrianingViewNetworkBool=False,
			_BrianingActivityStr="",
			_BrianingPrintBool=True,
			_BrianingMonitorIndexIntsList=None,
			_BrianingEventSelectVariable=None,
			_BrianingSpikeViewVariable = None,
			_BrianingViewBool = True,
			_BrianingWindowFloat = 10.,
			_BrianedEventTraceVariable=None,
			_BrianedTimeQuantityVariable=None,
			_BrianedNetworkVariable=None,
			_BrianedNeurongroupVariable=None,
			_BrianedSynapsesVariable=None,
			_BrianedStateMonitorVariable=None,
			_BrianedSpikeMonitorVariable=None,
			_BrianedRateMonitorVariable=None,
			_BrianedClockVariable=None,
			_BrianedParentSingularStr="",
			_BrianedRecordKeyStrsList=None,
			_BrianedUnitsInt=None,
			_BrianedParentDeriveBrianerStr="",
			_BrianedTraceDeriveBrianersList=None,
			_BrianedSynapsesDeriveBrianersList=None,
			_BrianedStateDeriveBrianersList=None,
			_BrianedSpikeDeriveBrianersList=None,
			_BrianedViewTraceBool=False,
			_BrianedTitleBool=False,
			_BrianedSpikesListsList=None,
			_BrianedParentNetworkDeriveBrianerVariable=None,
			_BrianedParentPopulationDeriveBrianerVariable=None,
			_BrianedParentInteractomeDeriveBrianerVariable=None,
			_BrianedParentInteractionDeriveBrianerVariable=None,
			_BrianedParentDeriveRecorderVariable=None,
			**_KwargVariablesDict
		):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def propertize_setBrianDebugTimeFloat(self,_ValueVariable):

		#Check
		if _ValueVariable>self._BrianDebugTimeFloat:

			###########
			#set
			PrintStr="#/##########################################/#\n"
			PrintStr+='      t='+str(_ValueVariable)+'\n'
			PrintStr+="#/##########################################/#\n"
			print PrintStr

		#set
		self._BrianDebugTimeFloat=_ValueVariable

		#debug
		'''
		self.debug(
			[
				'We have setted the _BrianDebugTimeFloat'
			]
		)
		'''

	def do_brian(self):

		#/#################/#
		# Determine if it is an inside structure or the top
		#

		#debug
		'''
		self.debug(
			[
				'We brian here',
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
			self.BrianedParentSingularStr=self.ParentedTotalSingularListDict.keys()[0]

		#debug
		'''
		self.debug(
			[
				'Ok',
				('self.',self,[
					'BrianedParentSingularStr'
				])
			]
		)
		'''

		#/########################/#
		# Network level
		# 

		#Check
		if (self.ParentDeriveTeamerVariable==None or 'Populations' in self.TeamDict or self.ParentDeriveTeamerVariable.TeamTagStr not in [
			'Clocks',
			'Traces',
			'Samples',
			'Events',
			'Rates',
			'Interactomes',
			'Interactions'
		]) and self.BrianedParentSingularStr!="Population":

			#debug
			'''
			self.debug(
				[
					'It is a Network level',
					'We set the brian network'
				]
			)
			'''

			#set
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
						'It is a network with a one level pop',
						'So set the neurongroup'
					]
				)
				'''

				#brianPopulation
				self.brianPopulation()

				#debug
				'''
				self.debug(
					[
						'We end to set the neuron group here'
					]
				)
				'''

			#/########################/#
			# structure
			# 

			#debug
			'''
			self.debug(
				[
					'We brian structure in all the brian children...',
					'but first make brianClock the clocks',
					'self.TeamDict["Clocks"].ManagementDict.keys()',
					str(self.TeamDict["Clocks"].ManagementDict.keys())
				]
			)
			'''

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
					'Events',
					'Rates',
					'Samples',
					'Interactomes',
					'Interactions'
				],
				'#all',
				_ManagerCommandSetList=['brian']
			)

			#debug
			'''
			self.debug(
				[
					'Ok we have brian structured all the brian children...',
				]
			)	
			'''

		else:

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

			#set
			BrianedMethodKeyStr='brian'+self.BrianedParentSingularStr

			#Check
			if hasattr(self,BrianedMethodKeyStr):

				#/########################/#
				# call the special brian<BrianedParentSingularStr> method
				#

				#debug
				'''
				self.debug(
					[
						'It is a '+self.BrianedParentSingularStr+' level',
						'We brian<BrianedParentSingularStr>'
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
						'Ok we have setted brian'+self.BrianedParentSingularStr
					]
				)
				'''		

		#debug
		'''
		self.debug(
			[
				'end of brian here'
			]
		)
		'''

	def brianNetwork(self):

		#/####################/#
		# init the Network
		#

		#maybe should import
		import brian2
		brian2.prefs.codegen.target = 'cython'

		#set
		self.BrianedNetworkVariable=brian2.Network()

		#get
		self.BrianedTimeQuantityVariable=getattr(
			brian2,
			self.BrianingTimeQuantityStr
		)

		#/####################/#
		# init a simulation clock
		#

		#debug
		'''
		self.debug(
			[
				'We set a simulation clock at least'
			]
		)
		'''

		#Check
		self.getTeamer(
			"Clocks"
		).getManager(
			"Simulation"
		)


	def brianClock(self):

		#/####################/#
		# Determine the parents
		#

		#get
		self.BrianedParentNetworkDeriveBrianerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

		#/####################/#
		# Set the brian clock
		#

		#import
		from brian2 import Clock

		#debug
		'''
		self.debug(
			[
				'We set the brian clock',
				('self.',self,['StructureTagStr'])
			]
		)
		'''

		#set
		if self.ManagementTagStr=="Simulation":

			#set
			BrianedStepTimeFloat=self.BrianedParentNetworkDeriveBrianerVariable.BrianingStepTimeFloat
		else:

			#set
			BrianedStepTimeFloat=0.1

		#init
		self.BrianedClockVariable=Clock(
			dt=BrianedStepTimeFloat*self.BrianedParentNetworkDeriveBrianerVariable.BrianedTimeQuantityVariable,
			#name=self.StructureTagStr
		)

		#debug
		'''
		self.debug(
			[
				'We have setted the clock',
				('self.',self,[
						'BrianedClockVariable'
							])
			]
		)
		'''

	def brianPopulation(self):

		#debug
		'''
		self.debug(
			[
				'It is a Neurongroup level, we set the Neurongroup',
				'We adapt the shape of BrianingNeurongroupDict',
				('self.',self,[
							'BrianingNeurongroupDict',
							'RecordingKeyVariable'
						])
			]
		)
		'''

		#/########################/#
		# Determine parents
		#

		#Check
		if self.ParentDeriveTeamerVariable!=None:

			#set the parent
			self.BrianedParentNetworkDeriveBrianerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

		else:

			#set the parent
			self.BrianedParentNetworkDeriveBrianerVariable=self

		#/################/#
		# Adapt the arg
		#

		#debug
		'''
		self.debug(
			[
				'Check for the Neurongroup dict ',
				('self.',self,[
						'BrianingNeurongroupDict'
					])
			]
		)
		'''

		#Check
		if 'N' not in self.BrianingNeurongroupDict:
			self.BrianingNeurongroupDict['N']=0

		#Check
		if 'model' not in self.BrianingNeurongroupDict:
			self.BrianingNeurongroupDict['model']=''

		#maybe should import
		from brian2 import NeuronGroup

		#debug
		'''
		self.debug(
			[
				('self.',self,[
							'BrianingNeurongroupDict'
							]),
				'We now set the model system Neurongroup if N>0 and model!=""'
			]
		)
		'''
		
		#/################/#
		# Set the brian neurongroup
		#

		#Check
		if self.BrianingNeurongroupDict['N'
			]>0 and self.BrianingNeurongroupDict['model']!="":

			#get
			BrianedClockVariable=self.BrianedParentNetworkDeriveBrianerVariable.TeamDict[
							'Clocks'
						].ManagementDict[
							'Simulation'
						].BrianedClockVariable

			#debug
			'''
			self.debug(
				[
					'We set the neurongroup',
					'BrianedClockVariable is ',
					str(BrianedClockVariable)
				]
			)
			'''

			#init
			self.BrianedNeurongroupVariable=NeuronGroup(
				**dict(
					self.BrianingNeurongroupDict,
					**{
						#'name':self.ParentedTotalPathStr.replace('/','_')+'_'+self.ManagementTagStr,
						'clock':BrianedClockVariable
					} 
				)
			)

			#debug
			'''
			self.debug(
				[
					'Ok we have setted the Neurongroup',
					('self.',self,[
								'BrianedNeurongroupVariable'
								])
				]
			)
			'''

			#/##################/#
			# Define a debug
			#

			#Check
			if self.BrianingDebugVariable>0:

				#import
				from brian2 import network_operation,ms

				@network_operation(
					dt=self.BrianingDebugVariable*self.BrianedParentNetworkDeriveBrianerVariable.BrianedTimeQuantityVariable
				)
				def debugNeurongroup():

					#call
					self.setDebugNeurongroup()
				
				#add
				self.BrianedParentNetworkDeriveBrianerVariable.BrianedNetworkVariable.add(
					debugNeurongroup
				)


			#/##################/#
			# Set some Traces to record
			#

			#Check
			if self.BrianingNeurongroupDict['N']>0:

				#/##################/#
				# team States first all the brian variables
				#

				#add
				BrianedRecordSkipKeyStrsList=self.BrianingRecordSkipKeyStrsList+[
					'lastspike',
					'not_refractory'
				]

				#Check
				self.BrianedRecordKeyStrsList=filter(
					lambda __BrianedRecordKeyStr:
					__BrianedRecordKeyStr not in BrianedRecordSkipKeyStrsList,
					self.BrianedNeurongroupVariable.equations._equations.keys()
				)

				#debug
				'''
				self.debug(
					[
						'We have setted the variable to record',
						('self.',self,[
							'BrianingRecordSkipKeyStrsList',
							'BrianedRecordKeyStrsList'
						])
					]
				)	
				'''
				
				#Check
				if len(self.BrianedRecordKeyStrsList)>0:

					#debug
					'''
					self.debug(
							[
								'We simulate with neurongroup',
								'adapt the initial conditions of all the brian variables',
								'so first we team Traces and put Recorders inside or get it and mapSet'
							]
						)
					'''

					#Check
					BrianedTracesManager=self.getTeamer(
							'Traces'
						)
		

					#debug
					'''
					self.debug(
						[
							'We set the tracers',
							('self.',self,['BrianedRecordKeyStrsList']),
							#'Recorder.RecordPrefixStr is '+str(Recorder.RecordPrefixStr),
							#'BrianedTracesManager is '+SYS._str(
							#	BrianedTracesManager
							#)
						]
					)
					'''

					#map
					self.BrianedTraceDeriveBrianersList=map(
							lambda __ManagementKeyStr,__RecordKeyStr:
							BrianedTracesManager.getManager(
									__ManagementKeyStr
								).mapSet(
									{
										'RecordingKeyVariable':getattr(
											self.BrianedNeurongroupVariable,
											__RecordKeyStr
										),
										'RecordKeyStr':__RecordKeyStr
									}
								),
							map(
								lambda __BrianedRecordKeyStr:
								Recorder.RecordPrefixStr+__BrianedRecordKeyStr,
								self.BrianedRecordKeyStrsList
							),
							self.BrianedRecordKeyStrsList
						)

					#debug
					"""
					self.debug(
						[
							"BrianedTracesManager.ManagementDict.keys() is ",
							str(BrianedTracesManager.ManagementDict.keys())
						]
					)
					"""

			#/##################/#
			# add in the net
			#

			#add
			self.BrianedParentNetworkDeriveBrianerVariable.BrianedNetworkVariable.add(
				self.BrianedNeurongroupVariable
			)

		#debug
		'''
		self.debug(
			[
				'End of brianPopulation'
			]
		)
		'''

	def brianInteraction(self):

		#/########################/#
		# Postlet level
		#  

		#debug
		'''
		self.debug(
			[
				'It is an Interaction level',
				('self.',self,[
							#'BrianingSynapsesDict'
							]
				)
			]
		)
		'''

		#/####################/#
		# Set the parent
		#

		#Check
		if self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable.BrianedParentSingularStr=='Interactome':

			#debug
			'''
			self.debug(
				[
					'We are in a projectome structure'
				]
			)
			'''

			#set
			self.BrianedParentInteractomeDeriveBrianerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

			#get
			self.BrianedParentPopulationDeriveBrianerVariable=self.BrianedParentInteractomeDeriveBrianerVariable.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

		else:

			#debug
			'''
			self.debug(
				[
					'There is no projectome structure'
				]
			)
			'''

			#get
			self.BrianedParentPopulationDeriveBrianerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

		#get
		self.BrianedParentNetworkDeriveBrianerVariable=self.BrianedParentPopulationDeriveBrianerVariable.BrianedParentNetworkDeriveBrianerVariable


		#/####################/#
		# Set the ConnectedTo Variable
		#

		#debug
		'''
		self.debug(
			[
				'Check if we have to get the connected to variable',
				('self.',self,['ConnectedToVariable'])
			]
		)
		'''

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
				self.BrianedParentPopulationDeriveBrianerVariable
			)

		#Check
		if self.ConnectedToVariable==None:

			#return
			return


		#/####################/#
		# Set the BrianedParentPopulationDeriveBrianerVariable
		#

		#debug
		'''
		self.debug(
			[
				'Do we have to make parent-brian the connected variable ?',
				'self.ConnectedToVariable.BrianedNeurongroupVariable is ',
				str(self.ConnectedToVariable.BrianedNeurongroupVariable)
			]
		)
		'''

		#Check 
		if self.ConnectedToVariable.BrianedNeurongroupVariable==None:

			#parent brian
			self.ConnectedToVariable.parent(
				).brian(
				)

		#set
		BrianedNameStr=self.BrianedParentPopulationDeriveBrianerVariable.StructureTagStr+'_To_'+self.ConnectedToVariable.StructureTagStr

		#debug
		'''
		self.debug(
			[
				'We set the synapses',
				('self.',self,[
						'BrianedParentPopulationDeriveBrianerVariable',
						'ConnectedToVariable'
					]),
				'self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable is ',
				str(self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable),
				'self.ConnectedToVariable.BrianedNeurongroupVariable is ',
				str(self.ConnectedToVariable.BrianedNeurongroupVariable),
				'Maybe we have to make brian the post',
				'BrianedNameStr is '+BrianedNameStr
			]
		)
		'''

		#import
		from brian2 import Synapses

		#Check
		if self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable!=None and self.ConnectedToVariable.BrianedNeurongroupVariable!=None:

			#get the clock
			BrianedClockVariable=self.BrianedParentNetworkDeriveBrianerVariable.TeamDict[
					'Clocks'
				].ManagementDict[
					'Simulation'
				].BrianedClockVariable

			#debug
			'''
			self.debug(
				[
					('self.',self,[
							'BrianingSynapsesDict'
						]),
					'BrianedClockVariable is '+str(BrianedClockVariable)
				]
			)
			'''

			#init
			self.BrianedSynapsesVariable=Synapses(
				source=self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable,
				target=self.ConnectedToVariable.BrianedNeurongroupVariable,
				clock=BrianedClockVariable,
				#name=BrianedNameStr.replace('/','_'),
				**self.BrianingSynapsesDict
			)

		else:

			#debug
			'''
			self.debug(
				[
					'The Synapse init didn t work...',
					'self.BrianedParentPopulationDeriveBrianerVariable.BrianingNeurongroupDict is ',
					SYS._str(self.BrianedParentPopulationDeriveBrianerVariable.BrianingNeurongroupDict),
					'self.ConnectedToVariable.BrianingNeurongroupDict is ',
					SYS._str(self.ConnectedToVariable.BrianingNeurongroupDict),
				]
			)
			'''
			
		#/####################/#
		# Connect options
		#

		#connect
		if type(self.BrianingConnectVariable)==float:

			#debug
			'''
			self.debug(
				[
					'we connect with a sparsity of ',
					('self.',self,[
						'BrianingConnectVariable'
					])
				]
			)
			'''

			#connect
			self.BrianedSynapsesVariable.connect(
				True,
				p=self.BrianingConnectVariable
			)

		#/####################/#
		# add to the structure
		#

		#debug
		'''
		self.debug(
			[
				'Add to the Network brian this Synapses',
				('self.',self,[
					'BrianedSynapsesVariable'
				])
			]
		)
		'''

		#add
		self.BrianedParentNetworkDeriveBrianerVariable.BrianedNetworkVariable.add(
			self.BrianedSynapsesVariable
		)

		#/##################/#
		# Define a debug
		#

		#Check
		if self.BrianingDebugVariable>0:

			#import
			from brian2 import network_operation,ms

			@network_operation(
				dt=self.BrianingDebugVariable*self.BrianedParentNetworkDeriveBrianerVariable.BrianedTimeQuantityVariable
			)
			def debugSynapses():
				
				#call
				self.setDebugSynapses()
			
			#add
			self.BrianedParentNetworkDeriveBrianerVariable.BrianedNetworkVariable.add(
				debugSynapses
			)

		#/##################/#
		# Set some Traces to record
		#

		#get
		BrianedPreUnitsInt=self.BrianedSynapsesVariable.source.N
		BrianedPostUnitsInt=self.BrianedSynapsesVariable.target.N

		#set
		self.BrianedUnitsInt=BrianedPreUnitsInt*BrianedPostUnitsInt

		#Check
		if self.BrianedUnitsInt>0 :

			#/##################/#
			# team States first all the brian variables
			#

			#debug
			'''
			self.debug(
				[
					('self.',self,[
							'BrianingRecordSkipKeyStrsList',
						]),
					'self.BrianedSynapsesVariable.equations._equations.keys() is ',
					str(self.BrianedSynapsesVariable.equations._equations.keys())
				]
			)
			'''

			#Check
			self.BrianedRecordKeyStrsList=filter(
				lambda __BrianedRecordKeyStr:
				__BrianedRecordKeyStr not in self.BrianingRecordSkipKeyStrsList  and __BrianedRecordKeyStr!='lastupdate' and self.getBrianRecordBool(
					__BrianedRecordKeyStr
				),
				self.BrianedSynapsesVariable.equations._equations.keys()
			)

			#debug
			'''
			self.debug(
				[
					'We have setted the variable to record',
					('self.',self,[
						'BrianingRecordSkipKeyStrsList',
						'BrianedRecordKeyStrsList'
					])
				]
			)
			'''

			#Check
			if len(self.BrianedRecordKeyStrsList)>0:

				#debug
				'''
				self.debug(
						[
							'adapt the initial conditions of all the brian variables',
							'so first we team Traces and put Recorders inside or get it and mapSet'
						]
					)
				'''

				#Check
				BrianedTracesManager=self.getTeamer(
					'Traces'
				)

	
				#debug
				'''
				self.debug(
					[
						'We set the tracers',
						('self.',self,['BrianedRecordKeyStrsList'])
					]
				)
				'''

				#map
				self.BrianedTraceDeriveBrianersList=map(
						lambda __ManagementKeyStr,__RecordKeyStr:
						BrianedTracesManager.manage(
								__ManagementKeyStr,
								{
									'RecordingKeyVariable':getattr(
										self.BrianedSynapsesVariable,
										__RecordKeyStr
									),
									'RecordKeyStr':__RecordKeyStr
								}
							).ManagedValueVariable
						if __ManagementKeyStr not in BrianedTracesManager.ManagementDict
						else BrianedTracesManager.ManagementDict[__ManagementKeyStr].mapSet(
							{
								'RecordingKeyVariable':getattr(
									self.BrianedSynapsesVariable,
									__RecordKeyStr
								),
								'RecordKeyStr':__RecordKeyStr
							}
						),
						map(
							lambda __BrianedRecordKeyStr:
							self.ManagementTagStr+'_'+Recorder.RecordPrefixStr+__BrianedRecordKeyStr,
							self.BrianedRecordKeyStrsList
						),
						self.BrianedRecordKeyStrsList
					)

				#debug
				self.debug(
					[
						"Now ",
						('self.',self,[
								'BrianedTraceDeriveBrianersList'
							])
					]
				)

				#Check
				for BrianedTraceDeriveBrianer in self.BrianedTraceDeriveBrianersList:

					#set
					BrianedSamplesDeriveBrianer=BrianedTraceDeriveBrianer.getTeamer(
						"Samples"
					)

					#Check
					if len(BrianedSamplesDeriveBrianer.ManagementDict)==0:

						#debug
						self.debug(
							[
								"We build a default Sample for ",
								str(BrianedSamplesDeriveBrianer)
							]
						)

						#get
						BrianedSamplesDeriveBrianer.getManager(
							'Default'
						).setAttr(
							'ViewingYScaleFloat',
							1000.
						)


						

	def setDebugNeurongroup(self):

		#/##################/#
		# build the print
		#

		#print
		PrintStr='At time t='+str(self.BrianedNeurongroupVariable.clock.t)+', \n'
		PrintStr+='SYS Object is : '+self.StructureTagStr+', \n'
		PrintStr+='Brian NeuronGroup is : '+self.BrianedNeurongroupVariable.name+' \n'

		#loop
		for __KeyStr in self.BrianedNeurongroupVariable.equations._equations.keys():

			#set
			PrintStr+=__KeyStr+" is "+str(
				getattr(
					self.BrianedNeurongroupVariable,
					__KeyStr
				)
			)+'\n'


		#add
		PrintStr+='\n'

		#/##################/#
		# add in the net
		#

		#set
		self.BrianedParentNetworkDeriveBrianerVariable.BrianDebugTimeFloat=self.BrianedNeurongroupVariable.clock.t

		#print
		print PrintStr

	def setDebugSynapses(self):

		#/##################/#
		# build the print
		#

		#init
		PrintStr='At time t='+str(self.BrianedSynapsesVariable.clock.t)+', \n'
		PrintStr+='SYS Object is : '+self.StructureTagStr+', \n'
		PrintStr+='Brian Synapses is : '+self.BrianedSynapsesVariable.name+' \n'

		#loop
		for __KeyStr in self.BrianedSynapsesVariable.equations._equations.keys():

			#set
			PrintStr+=__KeyStr+" is "+str(
				getattr(
					self.BrianedSynapsesVariable,
					__KeyStr
				)
			)+'\n'


		#add
		PrintStr+='\n'

		#/##################/#
		# add in the net
		#

		#set
		self.BrianedParentNetworkDeriveBrianerVariable.BrianDebugTimeFloat=self.BrianedSynapsesVariable.clock.t

		#print
		print PrintStr

	def brianTrace(self):

		#debug
		'''
		self.debug(
			[
				'It is a Trace level, we set the Samples',
				('self.',self,[
							#'RecordingKeyVariable',
							'RecordKeyStr'
						])
			]
		)
		'''

		#/####################/#
		# Set the parent
		#

		#set
		BrianedParentDeriveBrianer=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

		#Check
		if BrianedParentDeriveBrianer.BrianedNeurongroupVariable!=None:

			#debug
			'''
			self.debug(
				[
					'It is a trace in a neurongroup'
				]
			)
			'''

			#get
			self.BrianedParentPopulationDeriveBrianerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

			#get
			self.BrianedParentNetworkDeriveBrianerVariable=self.BrianedParentPopulationDeriveBrianerVariable.BrianedParentNetworkDeriveBrianerVariable

			#set
			self.BrianedParentDeriveBrianerStr="Population"

			#set
			BrianedRecordBool=BrianedParentDeriveBrianer.BrianedNeurongroupVariable.N>0

		elif BrianedParentDeriveBrianer.BrianedSynapsesVariable!=None:

			#debug
			'''
			self.debug(
				[
					'It is a trace in synapses'
				]
			)
			'''
			
			#get
			self.BrianedParentInteractionDeriveBrianerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

			#get
			self.BrianedParentNetworkDeriveBrianerVariable=self.BrianedParentInteractionDeriveBrianerVariable.BrianedParentNetworkDeriveBrianerVariable

			#set
			self.BrianedParentDeriveBrianerStr="Interaction"

			#set
			BrianedRecordBool=BrianedParentDeriveBrianer.BrianedUnitsInt>0

		else:

			#set
			BrianedRecordBool=False

		#debug
		"""
		self.debug(
			[
				'Ok it is a trace in...',
				('self.',self,[
						'BrianedParentDeriveBrianerStr'
					]),
				'BrianedRecordBool is ',
				str(BrianedRecordBool)
			]
		)
		"""

		#Check
		if BrianedRecordBool:
		
			#/####################/#
			# we record
			#

			#Check
			if self.BrianingRecordInitBool:

				#debug
				'''
				self.debug(
					[
						'We record here'
					]
				)
				'''


				#record
				self.recordTrace()

			#/###################/#
			# Build the samples and maybe one default moniter
			#

			#debug
			'''
			self.debug(
				[
					'Look if we have samples here',
					"'Samples' not in self.TeamDict is ",
					str('Samples' not in self.TeamDict)
				]
			)
			'''

			#Check
			BrianedSamplesDeriveTeamer=self.getTeamer('Samples')

			#Check
			if len(BrianedSamplesDeriveTeamer.ManagementDict)==0:
				BrianedSamplesDeriveTeamer.getManager('Default')

			#debug
			'''
			self.debug(
				[
					'Do we have to set a default moniter ?',
					#'len(self.BrianedParentPopulationDeriveBrianerVariable.BrianedRecordKeyStrsList) is ',
					#str(len(self.BrianedParentPopulationDeriveBrianerVariable.BrianedRecordKeyStrsList)),
					'self.BrianedParentPopulationDeriveBrianerVariable.BrianedRecordKeyStrsList) is ',
					str(self.BrianedParentPopulationDeriveBrianerVariable.BrianedRecordKeyStrsList),
					
				]
			)
			'''


			#Check
			if self.BrianedParentDeriveBrianerStr=="Population" :
			#and len(
			#	self.BrianedParentPopulationDeriveBrianerVariable.BrianedRecordKeyStrsList
			#)==1:

				#debug
				'''
				self.debug(
					[
						'BrianedSamplesDeriveTeamer.ManagementDict.keys() is',
						str(BrianedSamplesDeriveTeamer.ManagementDict.keys())
					]
				)
				'''

				#Check
				if 'Default' in BrianedSamplesDeriveTeamer.ManagementDict:

					#manage
					BrianedDefaultBrianer=BrianedSamplesDeriveTeamer.ManagementDict[
						'Default'
					]

					#debug
					'''
					self.debug(
						[
							'There is just one variable that we sample',
							'we have managed a Default',
							'BrianedDefaultBrianer.RecordingLabelVariable is ',
							str(BrianedDefaultBrianer.RecordingLabelVariable),
							('self.',self,[
									'RecordingLabelVariable'
								])
						]
					)
					'''
					#Check
					if BrianedDefaultBrianer.RecordingLabelVariable==None:

						#Check
						if self.BrianedParentPopulationDeriveBrianerVariable.RecordingLabelVariable!=None:

							#get
							BrianedDefaultBrianer.RecordingLabelVariable=self.BrianedParentPopulationDeriveBrianerVariable.RecordingLabelVariable[:]
						
						else:

							#set the record labels
							BrianedDefaultBrianer.RecordingLabelVariable=[
								0
							] if self.BrianedParentPopulationDeriveBrianerVariable.BrianingNeurongroupDict[
								'N'
							]>0 else []

						#brian
						BrianedDefaultBrianer.parent(
							).brian(
							)

					#debug
					'''
					self.debug(
						[
							'We have sette the default Brianer',
							'BrianedDefaultBrianer.RecordingLabelVariable is ',
							str(BrianedDefaultBrianer.RecordingLabelVariable)
						]
					)
					'''



			elif self.BrianedParentDeriveBrianerStr=="Interaction":

				#debug
				'''
				self.debug(
					[
						'This variable is plastic',
						'BrianedRecordBool is',
						str(BrianedRecordBool)
					]
				)
				'''

				#Check
				if BrianedRecordBool:

					#get
					BrianedDefaultBrianer=BrianedSamplesDeriveTeamer.getManager(
							'Default'
						)

					#Check
					if BrianedDefaultBrianer.RecordingLabelVariable==None:

						#init
						BrianedDefaultBrianer.RecordingLabelVariable=[0]

						#Check
						if self.BrianedParentInteractionDeriveBrianerVariable.RecordingLabelVariable!=None:

							#get
							BrianedDefaultBrianer.RecordingLabelVariable=self.BrianedParentInteractionDeriveBrianerVariable.RecordingLabelVariable
						
						else:

							#set the record labels
							BrianedDefaultBrianer.RecordingLabelVariable=[0] if self.BrianedParentInteractionDeriveBrianerVariable.BrianedUnitsInt>0 else []

						#brian
						BrianedDefaultBrianer.parent(
							).brian(
							)

	def getBrianRecordBool(self,_RecordKeyStr):

		#debug
		'''
		self.debug(
			[
				'We look if the synapses is plastic',
				('self.',self,[
						'ManagementTagStr',
						'RecordKeyStr'
					]),
				'self.BrianedParentInteractionDeriveBrianerVariable.BrianingSynapsesDict is ',
				str(self.BrianedParentInteractionDeriveBrianerVariable.BrianingSynapsesDict)
			]
		)
		'''
	
		#Check
		if _RecordKeyStr.startswith("Delta"):
			return True

		#Check
		if 'pre' in self.BrianingSynapsesDict:

			#map
			return any(
				map(
					lambda __EquationStr:
					__EquationStr.startswith(_RecordKeyStr),
					self.BrianingSynapsesDict[
						'pre'
					].split('\n')
				)
			)

		else:

			#set
			BrianedDeriveRecordKeyStr='d'+_RecordKeyStr

			#map
			return any(
				map(
					lambda __EquationStr:
					__EquationStr.startswith(BrianedDeriveRecordKeyStr),
					self.BrianingSynapsesDict[
						'model'
					].split('\n')
				)
			)

	def brianSample(self):

		#debug
		'''
		self.debug(
			[
				'It is a Sample State Moniter level',
				('self.',self,[
							'RecordingLabelVariable',
							'BrianingMonitorIndexIntsList'
						])
			]
		)
		'''
		
		#/####################/#
		# Set the parent
		#

		#get
		self.BrianedParentDeriveRecorderVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

		#debug
		'''
		self.debug(
			[
				'self.BrianedParentDeriveRecorderVariable.BrianedParentDeriveBrianerStr is ',
				str(self.BrianedParentDeriveRecorderVariable.BrianedParentDeriveBrianerStr)
			]
		)
		'''
		
		#Check
		if self.BrianedParentDeriveRecorderVariable.BrianedParentDeriveBrianerStr=="Interaction":

			#get
			self.BrianedParentInteractionDeriveBrianerVariable=self.BrianedParentDeriveRecorderVariable.BrianedParentInteractionDeriveBrianerVariable

			#get
			self.BrianedParentPopulationDeriveBrianerVariable=self.BrianedParentInteractionDeriveBrianerVariable.ConnectedToVariable


		else:

			#debug
			'''
			self.debug(
				[
					('self.',self,[
							'BrianedParentDeriveRecorderVariable'
						])
				]
			)
			'''

			#get
			self.BrianedParentPopulationDeriveBrianerVariable=self.BrianedParentDeriveRecorderVariable.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

		#get
		self.BrianedParentNetworkDeriveBrianerVariable=self.BrianedParentPopulationDeriveBrianerVariable.BrianedParentNetworkDeriveBrianerVariable

		#Check
		if self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable!=None:

			#/####################/#
			# Add in the monitor indexes
			#

			#debug
			'''
			self.debug(
				[
					'We add in the monitor index',
					('self.',self,[
							'RecordingLabelVariable',
							'BrianingMonitorIndexIntsList'
						])
				]
			)
			'''

			#if self.BrianingMonitorIndexIntsList==None:
			#	self.BrianingMonitorIndexIntsList=[]

			#map
			map(
				lambda __IndexInt:
				self.BrianingMonitorIndexIntsList.append(
					__IndexInt
				) if __IndexInt not in self.BrianingMonitorIndexIntsList
				else None,
				self.RecordingLabelVariable
			)

			#debug
			'''
			self.debug(
				[
					'If it is empty then just set with the zero index trace'
				]
			)
			'''
			
			#if self.BrianingMonitorIndexIntsList==None:
			#	self.BrianingMonitorIndexIntsList=[]

			#Check
			if len(self.BrianingMonitorIndexIntsList)==0:

				#set
				self.BrianingMonitorIndexIntsList=[0]
				self.RecordingLabelVariable=self.BrianingMonitorIndexIntsList

			#/####################/#
			# Set the brian monitor
			#
		
			#debug
			'''
			self.debug(
				[
					'We set the state monitor',
					('self.',self,[
							#'BrianedParentPopulationDeriveBrianerVariable'
							'RecordingLabelVariable',
							'BrianingMonitorIndexIntsList'
						]),
					'self.BrianedParentDeriveRecorderVariable.RecordKeyStr is ',
					str(self.BrianedParentDeriveRecorderVariable.RecordKeyStr),
					#'self.ParentedTotalManagementOrderedDict.keys() is ',
					#str(self.ParentedTotalManagementOrderedDict.keys()),
					'self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable.N is '+str(
						self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable.N
					)
				]
			)
			'''

			#Check
			if self.BrianedParentDeriveRecorderVariable.RecordKeyStr=="":
				self.BrianedParentDeriveRecorderVariable.RecordKeyStr=self.ParentGrandManagementTagStr

			#get
			BrianedBrianVariable=self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable if self.BrianedParentDeriveRecorderVariable.BrianedParentDeriveBrianerStr=="Population" else self.BrianedParentInteractionDeriveBrianerVariable.BrianedSynapsesVariable

			#get
			BrianArrayVariable=getattr(
				BrianedBrianVariable,
				self.BrianedParentDeriveRecorderVariable.RecordKeyStr
			)

			#debug
			'''
			self.debug(
				[
					'BrianedBrianVariable is '+str(BrianedBrianVariable),
					'BrianArrayVariable is '+str(BrianArrayVariable)
				]
			)
			'''

			#Check
			if len(
				self.BrianingMonitorIndexIntsList
			)>len(BrianArrayVariable):
			
				#cut
				BrianedMonitorIndexIntsList=self.BrianingMonitorIndexIntsList[
					:len(BrianArrayVariable)
				]
			else:

				#alias
				BrianedMonitorIndexIntsList=self.BrianingMonitorIndexIntsList


			#import
			from brian2 import StateMonitor

			#Check
			if self.BrianedParentDeriveRecorderVariable.RecordKeyStr=="":
				self.BrianedParentDeriveRecorderVariable.RecordKeyStr=self.BrianedParentDeriveRecorderVariable.ManagementTagStr

			#debug
			'''
			self.debug(
				[
					"We init the StateMonitor",
					"self.BrianedParentDeriveRecorderVariable.RecordKeyStr is "+str(
						self.BrianedParentDeriveRecorderVariable.RecordKeyStr)
				]
			)
			'''
			
			#init
			self.BrianedStateMonitorVariable=StateMonitor(
					BrianedBrianVariable,
					self.BrianedParentDeriveRecorderVariable.RecordKeyStr,
					BrianedMonitorIndexIntsList
				)

			#debug
			'''
			self.debug(
				[
					'Ok we have setted the monitor',
					('self.',self,['BrianedStateMonitorVariable']),
					'Now we add to the structure',
					'self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable is ',
					str(self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable)
				]
			)
			'''

			#/####################/#
			# add to the structure
			#

			#debug
			'''
			self.debug(
				[
					'We add to the structure'
				]
			)
			'''

			#add
			self.BrianedParentNetworkDeriveBrianerVariable.BrianedNetworkVariable.add(
				self.BrianedStateMonitorVariable
			)

			#/####################/#
			# record
			#

			#record
			self.recordSample()

	def brianEvent(self):

		#debug
		'''
		self.debug(
			[
				'It is a Spike Moniter level',
				('self.',self,[
							])
			]
		)
		'''

		#/####################/#
		# Set the BrianedParentPopulationDeriveBrianerVariable
		#

		#get
		self.BrianedParentPopulationDeriveBrianerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

		#get
		self.BrianedParentNetworkDeriveBrianerVariable=self.BrianedParentPopulationDeriveBrianerVariable.BrianedParentNetworkDeriveBrianerVariable

		#Check
		if self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable!=None:

			#/####################/#
			# Set the brian monitor
			#
		
			#debug
			'''
			self.debug(
				[
					'We set the spike monitor'
				]
			)
			'''

			#import
			from brian2 import SpikeMonitor

			#init
			self.BrianedSpikeMonitorVariable=SpikeMonitor(
					self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable,
				)

			#debug
			'''
			self.debug(
				[
					'Ok we have setted the monitor',
					('self.',self,['BrianedSpikeMonitorVariable']),
					'Now we add to the structure',
					'self.BrianedParentPopulationDeriveBrianerVariable.BrianedNetworkVariable is ',
					str(self.BrianedParentPopulationDeriveBrianerVariable.BrianedNetworkVariable)
				]
			)
			'''

			#/####################/#
			# add to the structure
			#

			#add
			self.BrianedParentNetworkDeriveBrianerVariable.BrianedNetworkVariable.add(
				self.BrianedSpikeMonitorVariable
			)


	def brianRate(self):

		#debug
		'''
		self.debug(
			[
				'It is a Rate Moniter level',
				('self.',self,[
								'ManagementTagStr'
							])
			]
		)
		'''
		
		#/####################/#
		# Set the BrianedParentPopulationDeriveBrianerVariable
		#

		#get
		self.BrianedParentPopulationDeriveBrianerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

		#get
		self.BrianedParentNetworkDeriveBrianerVariable=self.BrianedParentPopulationDeriveBrianerVariable.BrianedParentNetworkDeriveBrianerVariable


		#/####################/#
		# Check for a rate monitor
		#

		#import
		from brian2 import PopulationRateMonitor

		#init
		self.BrianedRateMonitorVariable=PopulationRateMonitor(
			self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable,
		)


		#/####################/#
		# add to the structure
		#

		#add
		self.BrianedParentNetworkDeriveBrianerVariable.BrianedNetworkVariable.add(
			self.BrianedRateMonitorVariable
		)

	def mimic_view(self):

		#debug
		self.debug(
			[
				"We mimic_view here"
			]
		)

		#/########################/#
		# Network level
		# 

		#Check
		if (self.ParentDeriveTeamerVariable==None or 'Populations' in self.TeamDict or self.ParentDeriveTeamerVariable.TeamTagStr not in [
			'Clocks',
			'Traces',
			'Samples',
			'Events',
			'Rates',
			'Interactomes',
			'Interactions'
		]) and self.BrianedParentSingularStr!="Population":

			#debug
			'''
			self.debug(
				[
					'It is a Network level',
					'We structure view'
				]
			)
			'''

			#/########################/#
			# Do we need
			# 

			#Check
			#if self.BrianedNetworkVariable==None:
			#	return

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
						'So viewPopulation'
					]
				)
				'''
				
				#viewPopulation
				self.viewPopulation()

				#debug
				'''
				self.debug(
					[
						'We end to viewPopulation for this network'
					]
				)
				'''

			else:

				#debug
				'''
				self.debug(
					[
						'It is a network ',
						'We build a Panel'
					]
				)
				'''

				#/########################/#
				# Build a Panel Run Charts 
				#

				#get
				self.getTeamer(
						"Panels"
					).getManager(
						"Run"
					).getTeamer(
						"Charts"
					)

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
					'Rates',
					'Samples',
					'Interactomes',
					'Interactions'
				],
				'#all',
				_ManagerCommandSetList=[
					'view'
				]
			)

			#debug
			'''
			self.debug(
				[
					'Ok we have view structured all the brian children...',
				]
			)	
			'''

			#Check
			if 'Populations' in self.TeamDict:

				#set
				self.viewNetwork()

		elif self.BrianedParentSingularStr!="":

			#set
			BrianedMethodKeyStr='view'+self.BrianedParentSingularStr

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
						'Ok we have setted view'+self.BrianedParentSingularStr
					]
				)
				'''	

		#debug
		'''
		self.debug(
			[
				'End of mimic_view'
			]
		)
		'''

	def viewNetwork(self):
		pass

	def viewPopulation(self):

		#debug
		'''
		self.debug(
			[
				'we view population brian here',
				('self.',self,[
						'BrianingViewNetworkBool'
					])
			]
		)
		'''

		#Check
		if self.BrianingViewNetworkBool==False:

			#/################/#
			# Build the Panels Charts to welcome the axes
			#

			#debug
			'''
			self.debug(
				[
					'viewPopulation',
					'We complete a view so first fill the draw',
					('self.',self,[
							'StructureTopDeriveStructurerRigidVariable',
							'StructuringManagerCommandSetList'
						])
				]
			)
			'''

			#Check
			self.getTeamer(
					"Panels"
				).getManager(
					"Run"
				).getTeamer(
					"Charts"
				)

			#/################/#
			# Check if it was during a structure call or not
			#

			#Check
			if self.StructureTopDeriveStructurerRigidVariable==None: 

				#debug
				'''
				self.debug(
					[
						'It was not during a structuring call so structure from this level to down'
					]
				)
				'''

				#structure
				self.structure(
					[
						'Traces',
						'Events',
						'Samples',
						'Interactomes',
						'Interactions'
					],
					'#all',
					_ManagerCommandSetList=[
						'view'
					]
				)

				#debug
				'''
				self.debug(
					[
						'End of structuring'
					]
				)
				'''

		#Check
		else:

			#/################/#
			# Update the Run Panel in the Network
			#

			#debug
			"""
			self.debug(
				[
					"We look for a Panels in BrianedParentNetworkDeriveBrianerVariable"
				]
			)
			"""
			
			#Check
			if "Panels" in self.BrianedParentNetworkDeriveBrianerVariable.TeamDict:

				#debug
				'''
				self.debug(
					[
						'We update the Run Panel in the Network',

					]
				)
				'''

				#get
				ViewedNetworkRunDerivePyploter=self.BrianedParentNetworkDeriveBrianerVariable.TeamDict[
					"Panels"
				].ManagementDict[
					"Run"
				]

				#get
				ViewedNetworkRunChartsManager=ViewedNetworkRunDerivePyploter.TeamDict[
					"Charts"
				]

				#/################/#
				# Transfer or not some properties
				#

				#debug
				'''
				self.debug(
					[
						'Are we going to transfer things',
						('self.',self,[
								'PyplotingShapeVariable',
								'PyplotingShiftVariable'
							])
					]
				)
				'''

				#Check
				if self.PyplotingShapeVariable==None:

					#Check
					if ViewedNetworkRunDerivePyploter.PyplotingShapeVariable!=None:

						#copy
						self.PyplotingShapeVariable = ViewedNetworkRunDerivePyploter.PyplotingShapeVariable[:]

					#Check
					else:

						#default
						self.PyplotingShapeVariable = [5,17]

				#debug
				'''
				self.debug(
					[
						'In the start',
						('self.',self,[
								'PyplotingShiftVariable',
								'ManagementIndexInt'
							])
					]
				)
				'''

				#Check
				if self.PyplotingShiftVariable==None:

					#debug
					'''
					self.debug(
						[
							'ViewedNetworkRunDerivePyploter.PyplotingShiftVariable is ',
							str(ViewedRunDerivePyploter.PyplotingShiftVariable)
						]
					)
					'''

					#Check
					if ViewedNetworkRunDerivePyploter.PyplotingShiftVariable!=None:

						#copy
						self.PyplotingShiftVariable = ViewedNetworkRunDerivePyploter.PyplotingShiftVariable[:]

					#Check
					else:

						#default
						self.PyplotingShiftVariable=[3,0]

				#debug
				'''
				self.debug(
					[
						'In the end',
						('self.',self,[
								'PyplotingShiftVariable'
							])
					]
				)
				'''

				#/################/#
				# Manage each Chart
				#

				#get
				ViewedPopulationRunChartsDerivePyploter=self.TeamDict[
					"Panels"
				].ManagementDict[
					"Run"
				].TeamDict[
					"Charts"
				]

				#get
				ViewedPopulationRunChartDerivePyplotersList=ViewedPopulationRunChartsDerivePyploter.ManagementDict.values()

				#debug
				LeakedTagVariable=map(
					lambda __Variable:
					(__Variable.ManagementIndexInt,
					__Variable.ManagementTagStr),
					ViewedPopulationRunChartDerivePyplotersList
				)

				'''
				#debug
				self.debug(
					[
						'We map manage each Chart in the network one',
						'ViewedPopulationRunChartsDerivePyploter.ManagementDict.keys() is',
						str(ViewedPopulationRunChartsDerivePyploter.ManagementDict.keys()
							),
						'LeakedTagVariable is '+str(LeakedTagVariable)
					]
				)
				'''

				#map
				ViewedNetworkRunChartDerivePyplotersList=map(
					lambda __ViewedPopulationRunChartDerivePyploter:
					ViewedNetworkRunChartsManager.getManager(
						self.ManagementTagStr+'_'+ __ViewedPopulationRunChartDerivePyploter.ManagementTagStr,
					),
					ViewedPopulationRunChartDerivePyplotersList
				)

				#debug
				'''
				self.debug(
					[
						'We are going to transfer',
						('self.',self,[
							'PyplotingShiftVariable',
							'PyplotingShapeVariable'
						])
					]
				)
				'''
				
				#/################/#
				# Look at transfering legend
				#

				#debug
				'''
				self.debug(
					[
						'Are we tranfering some legends'
					]
				)
				'''

				#map
				map(
					lambda __ViewedNetworkRunChartDerivePyplotersList,__ViewedPopulationRunChartDerivePyploter:
					__ViewedNetworkRunChartDerivePyplotersList.setAttr(
						'PyplotingLegendDict',
						__ViewedPopulationRunChartDerivePyploter.PyplotingLegendDict
					) 
					if __ViewedNetworkRunChartDerivePyplotersList.PyplotingLegendDict==None
					else None,
					ViewedNetworkRunChartDerivePyplotersList,
					ViewedPopulationRunChartDerivePyplotersList
				)

				#/################/#
				# Look at transfering other things
				#
				
				#map
				map(
					lambda __DeriveChartPyploter,__IndexInt:
					ViewedNetworkRunChartsManager.getManager(
						self.ManagementTagStr+'_'+ __DeriveChartPyploter.ManagementTagStr,
					).mapSetAttr(
						{
							'PyplotingXSkipTickBool':True,
							'PyplotingShiftVariable':self.PyplotingShiftVariable if __IndexInt==0 else [2,0],
							'PyplotingChartVariable':__DeriveChartPyploter.PyplotingChartVariable,
							'PyplotingShapeVariable':self.PyplotingShapeVariable,
						}
					).mapSetAttr(
						map(
							lambda __KeyStr:
							(
								__KeyStr,
								getattr(
									__DeriveChartPyploter,
									__KeyStr
								)
							),
							BrianViewKeyStrsList
						)
					).view(
					).getTeamer(
						'Draws'
					).mapManage(
						map(
							lambda __ItemTuple:
							(
								__ItemTuple[0],
								{
									'PyplotingDrawVariable':__ItemTuple[1].PyplotingDrawVariable
								}
							),
							__DeriveChartPyploter.TeamDict['Draws'].ManagementDict.items()
						)
					),
					ViewedPopulationRunChartDerivePyplotersList,
					xrange(len(ViewedPopulationRunChartDerivePyplotersList))
				)

				#Set a gap
				if len(ViewedNetworkRunChartsManager.ManagementDict)>0:

					#set
					ViewedNetworkRunChartsManager.ManagementDict.getValue(
						0
					).PyplotingShiftIntsTuple=[2,0]

	def viewInteraction(self):

		#debug
		'''
		self.debug(
			[
				'we view interaction brian here',
				('self.',self,[
						'BrianingViewNetworkBool'
					])
			]
		)
		'''

		#Check
		if self.BrianingViewNetworkBool==False:

			#/################/#
			# Build the Panels Charts to welcome the axes
			#

			#debug
			'''
			self.debug(
				[
					'viewInteraction',
					'We complete a view so first fill the draw',
					('self.',self,[
							'StructureTopDeriveStructurerRigidVariable',
							'StructuringManagerCommandSetList'
						])
				]
			)
			'''

		#Check
		#print(self.BrianedParentPopulationDeriveBrianerVariable['/-Panels/|Run/-Charts'])
		
		#/################/#
		# Just rerender the view Population
		#

		#call
		self.BrianedParentPopulationDeriveBrianerVariable.viewPopulation()

	def viewTraceOrEvent(self):

		#debug
		'''
		self.debug(
			[
				'We viewTraceOrEvent here',
				('self.',self,['ManagementIndexInt']),
				"len(self.ParentDeriveTeamerVariable.ManagementDict)-1 is ",
				len(self.ParentDeriveTeamerVariable.ManagementDict)-1,
				"self.ParentDeriveTeamerVariable.ManagementDict.keys() is ",
				self.ParentDeriveTeamerVariable.ManagementDict.keys()
			]
		)
		'''

		#Check
		if self.ManagementIndexInt==len(
			self.ParentDeriveTeamerVariable.ManagementDict
		)-1:

			#debug
			'''
			self.debug(
				[
					'Are we going to make the parent view',
					"self.BrianedParentPopulationDeriveBrianerVariable==None is "+str(
						self.BrianedParentPopulationDeriveBrianerVariable==None),
					"self.BrianedParentInteractionDeriveBrianerVariable==None is "+str(
						self.BrianedParentInteractionDeriveBrianerVariable==None),
				]
			)
			'''

			#Check
			#if self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable.BrianedSynapsesVariable!=None:
			#	self.BrianedParentInteractionDeriveBrianerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

			#Check
			if self.BrianedParentInteractionDeriveBrianerVariable==None and self.BrianedParentPopulationDeriveBrianerVariable!=None:

				#Check
				'''
				self.debug(
					[
						'This is the last Recorder for this population in this sample',
						'We redo viewPopulation in the Population'
					]
				)
				'''
				
				#Check
				if self.BrianedParentPopulationDeriveBrianerVariable!=self.BrianedParentNetworkDeriveBrianerVariable:

					#debug
					'''
					self.debug(
						[
							"Yes we redo view in the parent population"
						]
					)
					'''

					#set
					self.BrianedParentPopulationDeriveBrianerVariable.BrianingViewNetworkBool=True
					self.BrianedParentPopulationDeriveBrianerVariable.viewPopulation()

			#Check
			if self.BrianedParentInteractionDeriveBrianerVariable!=None:

				#Check
				'''
				self.debug(
					[
						'This is the last Recorder for this interaction in this sample',
						'We redo viewInteraction in the Population',
						"self.BrianedParentInteractionDeriveBrianerVariable.viewInteraction is "+str(
							self.BrianedParentInteractionDeriveBrianerVariable.viewInteraction)
					]
				)
				'''

				#set
				self.BrianedParentInteractionDeriveBrianerVariable.BrianingViewNetworkBool=True
				self.BrianedParentInteractionDeriveBrianerVariable.viewInteraction()


	def viewSample(self):

		#debug
		'''
		self.debug(
			[
				'viewSample',
				'self.BrianedParentDeriveRecorderVariable.BrianingRecordInitBool is ',
				str(self.BrianedParentDeriveRecorderVariable.BrianingRecordInitBool),
				'self.BrianedParentPopulationDeriveBrianerVariable.BrianedRecordKeyStrsList is ',
				str(self.BrianedParentPopulationDeriveBrianerVariable.BrianedRecordKeyStrsList),
				'self.BrianedParentDeriveRecorderVariable.ManagementTagStr is ',
				str(self.BrianedParentDeriveRecorderVariable.ManagementTagStr),
				'self.BrianedParentInteractionDeriveBrianerVariable!=None is ',
				str(self.BrianedParentInteractionDeriveBrianerVariable!=None)
			]
		)
		'''

		#Check
		if self.BrianedParentInteractionDeriveBrianerVariable!=None:

			#map
			ViewedRecordKeyStrsList = map(
				lambda __BrianedRecordKeyStr:
				self.BrianedParentInteractionDeriveBrianerVariable.ManagementTagStr+'_'+__BrianedRecordKeyStr,
				self.BrianedParentInteractionDeriveBrianerVariable.BrianedRecordKeyStrsList
			)
			ViewedBrianVariable = self.BrianedParentInteractionDeriveBrianerVariable.BrianedSynapsesVariable
		else:

			#set
			ViewedRecordKeyStrsList = self.BrianedParentPopulationDeriveBrianerVariable.BrianedRecordKeyStrsList
			ViewedBrianVariable = self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable

		#debug
		'''
		self.debug(
			[
				'ViewedRecordKeyStrsList is '+str(ViewedRecordKeyStrsList)
			]
		)
		'''

		#Check
		if SYS.deprefix(
				self.BrianedParentDeriveRecorderVariable.ManagementTagStr,
				Recorder.RecordPrefixStr
			) not in ViewedRecordKeyStrsList:

			#debug
			'''
			self.debug(
				[
					'self.BrianedParentDeriveRecorderVariable.ManagementTagStr not in ViewedRecordKeyStrsList',
					'we return'
				]
			)
			'''

			#return
			return self

		#debug
		'''
		self.debug(
			[
				'We complete a view so first fill the draw',
				('self.',self,[
					'RecordingLabelVariable',
					'ViewedLegendLabelStr',
					'StructureTopDeriveStructurerRigidVariable'
				])
			]
		)
		'''

		#/##################/#
		# If there is just one plot
		#

		#init
		self.PyplotingFigureVariable={
			'figsize':(14,4)
		}

		#/##################/#
		# Determine the way of labeling the variable names
		#

		#set
		if self.ViewedLegendLabelStr=="":

			#debug
			'''
			self.debug(
				[
					'Determine the legend label',
					'self.BrianedParentDeriveRecorderVariable.BrianingActivityStr is ',
					self.BrianedParentDeriveRecorderVariable.BrianingActivityStr
				]
			)
			'''

			#set
			self.ViewedLegendLabelStr='$'+self.getLabelStr(
				self.BrianedParentDeriveRecorderVariable.BrianingActivityStr
			) if self.BrianedParentDeriveRecorderVariable.BrianingActivityStr!="" else '$'+self.getLabelStr(
				self.BrianedParentDeriveRecorderVariable.RecordKeyStr
			)
			
			'''
			self.ViewedLegendLabelStr+='_{'+str(	
					#self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable.name
					#self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable.
					
				).replace('_','/')+'}'
			'''

			#debug
			'''
			self.debug(
				[
					'We have specified the legend label',
					('self.',self,[
						'ViewedLegendLabelStr'
					])
				]
			)
			'''


		#/##################/#
		# add a zero y line
		#

		#list
		if len(self.BrianedStateMonitorVariable.t)==0:
			return 

		#check
		self.PyplotingDrawVariable=[
			(
				'plot',
				{
					'#liarg':[
						[
							self.BrianedStateMonitorVariable.t[0],
							self.BrianedStateMonitorVariable.t[-1]
						],
						[0.,0.]
					],
					'#kwarg':dict(
						{
							'linestyle':'--',
							'linewidth':1,
							'color':'black'
						}
					)
				}
			)
		]


		#/##################/#
		# add the traces
		#

		#debug
		'''
		self.debug(
			[
				'we set the PyplotingDrawVariable',
				('self.',self,[
						'RecordedColorTuplesList',
						'RecordingLabelVariable',
						'BrianingPyplotDict'
					])
			]
		)
		'''

		#import
		import numpy as np

		#len
		BrianedMonitorsInt=len(
			np.array(
				getattr(
					self.BrianedStateMonitorVariable,
					self.BrianedParentDeriveRecorderVariable.RecordKeyStr
				)
			)
		)

		#debug
		'''
		self.debug(
			[
				('self.',self,[
						'RecordingLabelVariable'
					]),
				'BrianedMonitorsInt is '+str(BrianedMonitorsInt)
			]
		)
		'''

		#Check
		if len(self.RecordingLabelVariable)>BrianedMonitorsInt:
			RecordedLabelVariable=self.RecordingLabelVariable[:BrianedMonitorsInt]
		else:
			RecordedLabelVariable=self.RecordingLabelVariable

		#debug
		'''
		self.debug(
			[
				"RecordedLabelVariable is "+str(RecordedLabelVariable)
			]
		)
		'''
		
		#/####################/#
		# maybe set scale
		#

		#get
		ViewingYVariable=getattr(
						self.BrianedStateMonitorVariable,
						self.BrianedParentDeriveRecorderVariable.RecordKeyStr
				)

		#split
		BrianedActivityUnit=getattr(
				ViewedBrianVariable,
				self.BrianedParentDeriveRecorderVariable.RecordKeyStr
			).unit

		#divide
		self.ViewingYVariable=ViewingYVariable/(
			BrianedActivityUnit
		)

		#self.ViewingYVariable=ViewingYVariable
		self.ViewingYVariable=self.ViewingYVariable[:]

		#Check
		if str(BrianedActivityUnit)=='1':
			self.ViewingYVariable=self.ViewingYVariable/self.ViewingYScaleFloat


		#debug
		'''
		self.debug(
			[
				'ViewingYVariable is '+str(ViewingYVariable)
			]
		)
		'''

		#max
		ViewedMinFloat=self.ViewingYVariable.max()-(
			abs(self.ViewingYVariable.max()-self.ViewingYVariable.min())/2.
			)
		ViewedMaxFloat=self.ViewingYVariable.max()+abs(
			self.ViewingYVariable.max()-self.ViewingYVariable.min()
		)

		#/####################/#
		# define the plot
		#

		#set
		self.PyplotingDrawVariable+=map(
			lambda __IndexInt,__SelectInt:
			(
				'plot',
				{
					'#liarg:#map@get':[
						'#IdGetStr.BrianedStateMonitorVariable.t',
						#'>>SYS.IdDict[#IdStr].BrianedStateMonitorVariable.'+self.BrianedParentDeriveRecorderVariable.RecordKeyStr+'['+str(
						#	__IndexInt)+',:]'
						'>>SYS.IdDict[#IdStr].ViewingYVariable['+str(
							__IndexInt)+',:]'
					],
					'#kwarg':dict(
						{
							'label':self.ViewedLegendLabelStr+'^{'+str(__SelectInt)+'}$'
							if self.BrianedParentInteractionDeriveBrianerVariable==None
							else self.ViewedLegendLabelStr+'^{'+str(
								__SelectInt/self.BrianedParentInteractionDeriveBrianerVariable.BrianedSynapsesVariable.target.N
							)+str(
								__SelectInt%self.BrianedParentInteractionDeriveBrianerVariable.BrianedSynapsesVariable.source.N
							)+'}$',
							'linestyle':'-',
							'linewidth':3,
							'color':self.RecordedColorTuplesList[__IndexInt],

						},
						**self.BrianingPyplotDict
					)
				}
			),
			xrange(len(RecordedLabelVariable)),
			RecordedLabelVariable
		)

		#debug
		'''
		self.debug(
			[
				'After set',
				('self.',self,[
						'PyplotingDrawVariable'
					])
			]
		)
		'''



		#/################/#
		# Add the event on the traces
		# (only for population trace)

		#Check
		if self.BrianedParentInteractionDeriveBrianerVariable==None and ViewedMinFloat!=ViewedMaxFloat:

			#Check
			if "Events" in self.BrianedParentPopulationDeriveBrianerVariable.TeamDict:

				#get
				BrianedSpikeMonitorVariable=self.BrianedParentPopulationDeriveBrianerVariable.TeamDict[
					"Events"
				].ManagementDict[
					"Default_Events"
				].BrianedSpikeMonitorVariable

				#debug
				'''
				self.debug(
					[
						'Look for spikes to plot on the traces',
						'BrianedSpikeMonitorVariable.i is '+str(
							BrianedSpikeMonitorVariable.i
						),
						'BrianedSpikeMonitorVariable.t is '+str(
							BrianedSpikeMonitorVariable.t
						),
						('self.',self,[
								'RecordedColorTuplesList'
							])
					]
				) 
				'''

				#import
				import numpy as np

				#Check
				if self.BrianedParentPopulationDeriveBrianerVariable.BrianingSpikeViewVariable==None :

					#set
					self.BrianedParentPopulationDeriveBrianerVariable.BrianingSpikeViewVariable=[
						ViewedMinFloat,ViewedMaxFloat
					]

				#debug
				'''
				self.debug(
					[
						"The size of the spikes to plot is ",
						"ViewedMinFloat,ViewedMaxFloat is ",str([ViewedMinFloat,ViewedMaxFloat]),
						"self.BrianedParentPopulationDeriveBrianerVariable.BrianingSpikeViewVariable is "+str(
							self.BrianedParentPopulationDeriveBrianerVariable.BrianingSpikeViewVariable)
					]
				)
				'''

				#add
				PyplotedSpikeTuplesList=SYS.filterNone(
					map(
						lambda __IndexInt,__FloatTime:
						(
							__IndexInt,
							(
								'plot',
								{
									'#liarg':[
										[__FloatTime,__FloatTime],
										self.BrianedParentPopulationDeriveBrianerVariable.BrianingSpikeViewVariable
									],
									'#kwarg':dict(
										{
											'linestyle':'-',
											'linewidth':2,
											'color':self.RecordedColorTuplesList[__IndexInt],

										},
										**self.BrianingPyplotDict
									)
								}
							)
						)
						if __IndexInt<len(self.RecordedColorTuplesList)
						else None,
						np.array(BrianedSpikeMonitorVariable.i),
						np.array(BrianedSpikeMonitorVariable.t)
					)
				)

				#/###############/#
				# So now we need to insert these plots between the plot traces
				#

				SpikeDict=dict(
					zip(
						self.RecordingLabelVariable,
						[[] for _Int in xrange(len(self.RecordingLabelVariable))]		
					)
				)

				#set
				map(
					lambda __PyplotedSpikeTuple:
					SpikeDict[
						__PyplotedSpikeTuple[0]
					].append(__PyplotedSpikeTuple[1]),
					PyplotedSpikeTuplesList
				)

				#debug
				'''
				self.debug(
					[
						'before the end, BE CAREFUL index are shifted with the --',
						'dashed black line',
						('self.',self,[
								'PyplotingDrawVariable'
							])
					]
				)
				'''

				#sum
				self.BrianedEventTraceVariable=map(
						lambda __IndexInt:
						[
							self.PyplotingDrawVariable[__IndexInt+1]
						]+SpikeDict[
							__IndexInt
						],
						RecordedLabelVariable
					)
				

				#link
				BrianedDefaultDeriveBrianerVariable=self.BrianedParentPopulationDeriveBrianerVariable.getTeamer(
					'Events'
				).getManager(
					'Default_Events'
				)
				BrianedDefaultDeriveBrianerVariable.BrianedEventTraceVariable=self.BrianedEventTraceVariable
				BrianedDefaultDeriveBrianerVariable.RecordingLabelVariable=self.RecordingLabelVariable

				#map
				self.PyplotingDrawVariable=[
					#add the null dashed line 
					self.PyplotingDrawVariable[0]
				]+SYS.sum(self.BrianedEventTraceVariable)
				
				#debug
				'''
				self.debug(
					[
						'In the end of adding events on the traces',
						('self.',self,[
								'PyplotingDrawVariable'
							])
					]
				)
				'''

		#/####################/#
		# maybe set for the Chart
		#

		#Debug
		"""
		self.debug(
			[
				"Should we init the PyplotingChartVariable",
				('self.',self,['PyplotingChartVariable'])
			]
		)
		"""

		#init
		self.PyplotingChartVariable=[
		]

		#/####################/#
		# maybe set the X Chart also
		#

		#get
		BrianedTimeUnit=self.BrianedStateMonitorVariable.t.unit

		#scale
		self.ViewingXVariable=self.BrianedStateMonitorVariable.t/(
			BrianedTimeUnit
		)

		#debug
		'''
		self.debug(
			[
				'We have putted without dimension the X time variable',
				('self.',self,[
						'ViewingXVariable'
					]
				)
			]
		)
		'''

		#set
		self.ViewingXLabelStr='$t\ ('+str(
			(1./self.ViewingXScaleFloat)*BrianedTimeUnit
		).split('.')[-1]+')$'
	
		#/####################/#
		# maybe set the Y Chart also
		#

		#debug
		'''
		self.debug(
			[
				'We set the y axis',
				'self.BrianedParentDeriveRecorderVariable.RecordedTraceFloatsArray is ',
				str(self.BrianedParentDeriveRecorderVariable.RecordedTraceFloatsArray)
			]
		)
		'''

		#Check
		if "Events" in self.BrianedParentPopulationDeriveBrianerVariable.TeamDict:
		
			#debug
			'''
			self.debug(
				[
					'We set the min and max of the viewing events Y variable',
					('self.',self,[
							'ViewingYVariable'
						])
				]
			)
			'''

			#set
			self.ViewingYVariable[0][0]=ViewedMaxFloat

		#set
		self.ViewingYLabelStr='$'+(
			self.getLabelStr(
				self.BrianedParentDeriveRecorderVariable.RecordKeyStr
			) if self.BrianedParentDeriveRecorderVariable.BrianingActivityStr=="" else self.getLabelStr(
				self.BrianedParentDeriveRecorderVariable.BrianingActivityStr
			) 
		)

		#debug
		'''
		self.debug(
			[
				"We scale the Y ",
				('self.',self,[
						'ViewingYScaleFloat'
					]),
				"BrianedActivityUnit is "+str(BrianedActivityUnit)
			]
		)
		'''

		#str
		ViewedDimensionStr=str(
			(1./self.ViewingYScaleFloat)*BrianedActivityUnit
		).split('.')[-1]

		#Check
		if str(BrianedActivityUnit)=='1':
			ViewedDimensionStr='1'
			#ViewedDimensionStr=str((1./self.ViewingYScaleFloat))

		#debug
		'''
		self.debug(
			[
				'set the ViewingYLabelStr',
				'self.BrianedParentDeriveRecorderVariable.BrianingActivityStr is ',
				str(self.BrianedParentDeriveRecorderVariable.BrianingActivityStr),
				'ViewedDimensionStr is '+ViewedDimensionStr,
				'BrianedActivityUnit is '+str(BrianedActivityUnit),
				('self.',self,['ViewingYScaleFloat'])
			]
		)
		'''

		#add
		self.ViewingYLabelStr+='\ ('+ViewedDimensionStr+')'
		self.ViewingYLabelStr+='$'

		#debug
		'''
		self.debug(
			[
				('self.',self,[
					'ViewingYLabelStr'
					])
			]
		)
		'''

		#/####################/#
		# Set the Chart globaly and look if we have to finish
		#

		#Check
		if self.ManagementIndexInt==len(self.ParentDeriveTeamerVariable.ManagementDict)-1:

			#Check
			if self.PyplotingLegendDict==None:
				self.PyplotingLegendDict={
					#'fontsize':10,
					#'ncol':2
				}

			#Check
			if self.BrianedParentNetworkDeriveBrianerVariable.PyplotingLegendDict!=None:

				#alias
				SYS.complete(
					self.PyplotingLegendDict,
					self.BrianedParentNetworkDeriveBrianerVariable.PyplotingLegendDict
				)

			#Check
			if self.BrianedParentPopulationDeriveBrianerVariable.PyplotingLegendDict!=None:

				#alias
				SYS.complete(
					self.PyplotingLegendDict,
					self.BrianedParentPopulationDeriveBrianerVariable.PyplotingLegendDict
				)

			#Check
			if 'ncol' not in self.PyplotingLegendDict:

				#set
				self.PyplotingLegendDict['ncol']=max(1,len(
						self.RecordingLabelVariable
					)/2)

			#debug
			'''
			self.debug(
				[
					'We give a legend to the Chart',
					('self.',self,[
							'PyplotingLegendDict'
						])
				]
			)
			'''
			
		#/################/#
		# call the base view method
		#

		#debug
		'''
		self.debug(
			[
				('self.',self,[
						'ViewingXVariable',
						'ViewingYVariable'
					]),
				'Now we call the view'
			]
		)	
		'''

		#call 
		BaseClass.view(self)
		
		#/####################/#
		# maybe replace Chart also
		#

		#debug
		'''
		self.debug(
			[
				'Before replace',
				('self.',self,[
					'PyplotingDrawVariable',
					'PyplotingChartVariable'
				])
			]
		)
		'''

		#mapReplace
		[
			self.PyplotingDrawVariable,
			self.PyplotingChartVariable
		]=map(
			lambda __Variable:
			SYS.replace(
				__Variable,
				{
					'#IdStr':str(self.PrintIdInt),
					'#IdGetStr':"#id:"+str(self.PrintIdInt)
				},
				self
			)
			if __Variable!=None
			else None,
			map(
				lambda __KeyStr:
				getattr(
					self,
					__KeyStr
				),
				[
					'PyplotingDrawVariable',
					'PyplotingChartVariable'
				]
			)
		)

		#debug
		'''
		self.debug(
			[
				'After replace',
				('self.',self,[
					#'PyplotingDrawVariable',
					'PyplotingChartVariable'
				])
			]
		)
		'''


		#/####################/#
		# Hook to escape 
		#

		#Check
		if self.BrianingViewBool == False or self.BrianedParentDeriveRecorderVariable.BrianingViewBool == False:
			
			#debug
			'''
			self.debug(
				[
					"We dont have to view this sample",
					('self.',self,[
							'ManagementTagStr'
						])
				]
			)
			'''
			
			#return
			return
			
		#/####################/#
		# Update maybe the 
		# parent neuron group

		#debug
		'''
		self.debug(
			[
				'Maybe we also update the view in the parent population',
				" \"Panels\" in self.BrianedParentPopulationDeriveBrianerVariable.TeamDict is ",
				str("Charts" in self.BrianedParentPopulationDeriveBrianerVariable.TeamDict)
			]
		)
		'''

		#Check
		if "Panels" in self.BrianedParentPopulationDeriveBrianerVariable.TeamDict:

			#debug
			'''
			self.debug(
				[
					"We update the parent neuron group view",
					"self.BrianedParentDeriveRecorderVariable.ManagementTagStr is ",
					self.BrianedParentDeriveRecorderVariable.ManagementTagStr
				]
			)
			'''

			#set
			BrianedRunPopulationChartsDeriveManager=self.BrianedParentPopulationDeriveBrianerVariable.TeamDict[
				"Panels"
			].ManagementDict[
				"Run"
			].TeamDict[
				"Charts"
			]

			#manage
			BrianedChartDerivePyploter=BrianedRunPopulationChartsDeriveManager.getManager(
				self.BrianedParentDeriveRecorderVariable.ManagementTagStr
			)

			#debug
			'''
			self.debug(
				[
					'We have managed this new Chart',
					'self.BrianedParentDeriveRecorderVariable.ManagementTagStr is '+str(
						self.BrianedParentDeriveRecorderVariable.ManagementTagStr),
					'BrianedRunPopulationChartsDeriveManager.ManagementDict is '+str(
						BrianedRunPopulationChartsDeriveManager.ManagementDict),
					'BrianedRunPopulationChartsDeriveManager.ManagementDict.keys() is '+str(
						BrianedRunPopulationChartsDeriveManager.ManagementDict.keys()
					)
				]
			)
			'''
			
			#/################/#
			# Set a title if it is the first Chart
			#

			#Check
			if self.BrianedParentPopulationDeriveBrianerVariable.ManagementTagStr!="":

				#debug
				'''
				self.debug(
					[
						"Do we print the title",
						('self.',self,[
								'ManagementIndexInt',
								'PyplotingChartVariable',
								'BrianingViewBool'
							]),
						"self.BrianedParentPopulationDeriveBrianerVariable.BrianedTitleBool is "+str(
							self.BrianedParentPopulationDeriveBrianerVariable.BrianedTitleBool),

					]
				)
				'''

				#Check
				if self.BrianedParentPopulationDeriveBrianerVariable.BrianedTitleBool==False:

					#Check
					if BrianedChartDerivePyploter.PyplotingChartVariable==None:
						BrianedChartDerivePyploter.PyplotingChartVariable=[]

					#set
					BrianedChartDerivePyploter.PyplotingChartVariable += [
						('set_title',
									{
										'#liarg':[
											'$'+self.BrianedParentPopulationDeriveBrianerVariable.ManagementTagStr+'$'
										],
										'#kwarg':{
											'fontsize':20
										}
									}
								)
					]

					#set
					self.BrianedParentPopulationDeriveBrianerVariable.BrianedTitleBool=True


			#/####################/#
			# set to True
			#

			#set
			BrianedChartDerivePyploter.PyplotingXSkipTickBool=True

			#/####################/#
			# Update the PyplotingLegendDict
			#

			#debug
			'''
			self.debug(
				[
					'We update a legend',
					('self.',self,[
							'PyplotingLegendDict'
						]),
					'BrianedChartDerivePyploter.ManagementTagStr is ',
					BrianedChartDerivePyploter.ManagementTagStr,
					'BrianedChartDerivePyploter.PyplotingLegendDict is ',
					str(BrianedChartDerivePyploter.PyplotingLegendDict)
				]
			)
			'''

			#alias
			if BrianedChartDerivePyploter.PyplotingLegendDict==None:

				#set
				BrianedChartDerivePyploter.PyplotingLegendDict=self.PyplotingLegendDict

			#/####################/#
			# Update the PyplotingChartVariable
			#

			#debug
			'''
			self.debug(
				[
					'Maybe we have to update the parent population chart',
					('self.',self,[
						'PyplotingChartVariable'
					]),
					'BrianedChartDerivePyploter.PyplotingChartVariable is ',
					str(BrianedChartDerivePyploter.PyplotingChartVariable)
				]
			)
			'''

			#update
			if BrianedChartDerivePyploter.PyplotingChartVariable==None:

				#alias
				BrianedChartDerivePyploter.PyplotingChartVariable=self.PyplotingChartVariable
			else:

				#extend
				BrianedChartDerivePyploter.PyplotingChartVariable.extend(
					self.PyplotingChartVariable
				)

			#update the view
			map(
				lambda __KeyStr:
				BrianedChartDerivePyploter.setAttr(
					__KeyStr,
					getattr(
						self,
						__KeyStr
					)
				),
				BrianViewKeyStrsList
			)
			BrianedChartDerivePyploter.view()

			#/####################/#
			# Team a Draws in this Chart
			#

			#debug
			'''
			self.debug(
				[
					'We update in the parent neurongroup chart',
					'BrianedChartDerivePyploter is ',
					SYS._str(BrianedChartDerivePyploter),
					('self.',self,[])
				]
			)
			'''

			#team
			BrianedDrawDeriveManager=BrianedChartDerivePyploter.getTeamer(
				'Draws'
			)

			#/####################/#
			# Manage a new draw
			#

			#debug
			'''
			self.debug(
				[
					('self.',self,[
							'ManagementIndexInt',
							'PyplotingDrawVariable'
						])
				]
			)
			'''

			#manage
			BrianedDrawDeriveManager.manage(
				str(self.ManagementIndexInt),
				{
					'PyplotingDrawVariable':self.PyplotingDrawVariable
				}
			)


		#/####################/#
		# Update maybe the 
		# network view

		#debug
		"""
		self.debug(
			[	
				"self.ParentDeriveTeamerVariable.ManagementDict.keys() is ",
				self.ParentDeriveTeamerVariable.ManagementDict.keys()
			]
		)
		"""

		#Check
		if self.ManagementIndexInt==len(
			self.ParentDeriveTeamerVariable.ManagementDict
		)-1:

			#Check
			"""
			self.debug(
				[
					'This is the last Sample for this record',
					'We viewTrace on the parent recorder (that will call viewPopulation)',
					"self.BrianedParentDeriveRecorderVariable.BrianedViewTraceBool is "+str(
						self.BrianedParentDeriveRecorderVariable.BrianedViewTraceBool
					)
				]
			)
			"""

			#call
			self.BrianedParentDeriveRecorderVariable.viewTraceOrEvent()

	def simulateEvent(self):

		#get
		self.BrianedSpikesListsList=[ [] for __IndexInt in xrange(
			self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable.N
			)
		]

		#loop
		for __IndexInt,__TimeUnit in zip(
			self.BrianedSpikeMonitorVariable.i,
			self.BrianedSpikeMonitorVariable.t
		):

			#append
			self.BrianedSpikesListsList[__IndexInt].append(
				__TimeUnit
				#100.*__TimeUnit/BrianedTimeUnit
				#float((1./self.ViewingXScaleFloat)*(__TimeUnit/BrianedTimeUnit))
				#float(__TimeUnit/BrianedTimeDimension)
			)


	def viewEvent(self):

		#/################/#
		# prepare the view
		#

		#get
		BrianedStateMonitorVariable=self.BrianedParentPopulationDeriveBrianerVariable.TeamDict[
			'Traces'
		].ManagementDict.getValue(
			0
		).TeamDict[
			'Samples'
		].ManagementDict.getValue(
			0
		).BrianedStateMonitorVariable

		#get
		BrianedTimeUnit=BrianedStateMonitorVariable.t.unit

		#debug
		'''
		self.debug(
			[
				'BrianedStateMonitorVariable is ',
				str(BrianedStateMonitorVariable)
			]
		)
		'''

		#set
		self.ViewingXVariable=BrianedStateMonitorVariable.t/BrianedTimeUnit

		#import
		import numpy as np

		#divide
		self.ViewingYVariable=np.array(self.BrianedSpikeMonitorVariable.i)

		#import
		import brian2

		#get
		BrianedTimeDimension=getattr(
			brian2,
			self.BrianedParentNetworkDeriveBrianerVariable.BrianingTimeQuantityStr
		)

		#debug
		"""
		self.debug(
			[
				"BrianedTimeDimension is ",str(BrianedTimeDimension),
				('self.',self,['ViewingXScaleFloat']),
				"self.BrianedSpikeMonitorVariable.i is "+str(self.BrianedSpikeMonitorVariable.i)
			]
		)
		"""

		

		#debug
		"""
		self.debug(
			[
				"Maybe we select specific spikes",
				('self.',self,['BrianingEventSelectVariable'])
			]
		)
		"""

		#select
		if self.BrianingEventSelectVariable!=None:

			#map
			BrianedSpikesListsList=map(
				lambda __BrianingEventNeuronInt:
				self.BrianedSpikesListsList[__BrianingEventNeuronInt],
				self.BrianingEventSelectVariable
			)

			#range
			self.ViewingYVariable=range(len(self.BrianingEventSelectVariable))
		else:
			BrianedSpikesListsList=self.BrianedSpikesListsList

		#debug
		"""
		self.debug(
			[
				"view Event",
				('self.',self,[
						'ViewingYVariable'
					]),
				#{self.BrianedSpikeMonitorVariable.__dict__ is ",str(np.array(
				#	self.BrianedSpikeMonitorVariable.__dict__)),
				'self.BrianedSpikesListsList is '+str(self.BrianedSpikesListsList)
			]
		)
		"""

		#set
		self.ViewingXLabelStr='$t\ ('+str(
			(1./self.ViewingXScaleFloat)*BrianedTimeUnit
		).split('.')[-1]+')$'

		#set
		self.ViewingYLabelStr='#$index$'
		
		#set
		self.ViewingYIndexBool=True
		self.ViewingYSampleInt=2

		#/################/#
		# call the base view method
		#

		#debug
		'''
		self.debug(
			[
				('self.',self,[
						'ViewingXVariable',
						'ViewingYVariable'
					]),
				'Now we call the view'
			]
		)
		'''

		#add mn and float
		self.ViewingAddYMinFloat=-1.
		self.ViewingAddYMaxFloat=1.

		#call 
		BaseClass.view(self)

		#/################/#
		# set pyplot draw
		#

		#debug
		'''
		self.debug(
			[
				'We complete a view so first fill the draw'
			]
		)
		'''

		#set
		ViewedLabelStr='$'+self.ManagementTagStr+'_{'+str(
			self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable.name
							).replace('_','/')+'}'

		#set
		self.PyplotingDrawVariable=[]
		"""
		self.PyplotingDrawVariable=[
			(
				'plot',
				{
					'#liarg:#map@get':[
						'#IdGetStr.BrianedSpikeMonitorVariable.t',
						'>>SYS.IdDict[#IdStr].ViewingYVariable'
					],
					'#kwarg':dict(
						{
							'label':ViewedLabelStr,
							'linestyle':'',
							'marker':'o',
							'color':'red',
							'markersize':5
						},
						**self.BrianingPyplotDict
					)
				}
			)
		]
		"""

		#/####################/#
		# maybe set global Chart also
		#

		#Check
		if self.PyplotingChartVariable==None:
			self.PyplotingChartVariable=[]

		#add
		self.PyplotingChartVariable+=[
			(
				'tick_params',{
					'#kwarg':{
						'length':10,
						'width':5,
						'which':'major'
					}
				}
			),
			(
				'tick_params',{
					'#kwarg':{
						'length':5,
						'width':2,
						'which':'minor'
					}
				}
			),
			('xaxis.set_ticks_position',
				{
					'#liarg':['bottom']
				}
			),
			('yaxis.set_ticks_position',
				{
					'#liarg':['left']
				}
			)
		]

		#/####################/#
		# maybe replace Chart also
		#

		#debug
		'''
		self.debug(
			[
				'Before replace',
				('self.',self,[
					'PyplotingDrawVariable',
					'PyplotingChartVariable'
				])
			]
		)
		'''

		#mapReplace
		[
			self.PyplotingDrawVariable,
			self.PyplotingChartVariable
		]=map(
			lambda __Variable:
			SYS.replace(
				__Variable,
				{
					'#IdStr':str(self.PrintIdInt),
					'#IdGetStr':"#id:"+str(self.PrintIdInt)
				},
				self
			)
			if __Variable!=None
			else None,
			map(
				lambda __KeyStr:
				getattr(
					self,
					__KeyStr
				),
				[
					'PyplotingDrawVariable',
					'PyplotingChartVariable'
				]
			)
		)

		#debug
		'''
		self.debug(
			[
				"Maybe there are the monitored trace inside",
				("self.",self,[
					'BrianedEventTraceVariable',
					'RecordingLabelVariable'
				])
			]
		)
		'''

		#Check
		if self.RecordingLabelVariable==None:
			self.RecordingLabelVariable=[0]

		#Check
		if self.BrianedEventTraceVariable==None:
			return

		#map
		self.PyplotingDrawVariable+=map(
			lambda __NeuronIndexInt:
			(
				'plot',
				{
					'#liarg':[
						BrianedSpikesListsList[__NeuronIndexInt],
						[__NeuronIndexInt]*len(self.BrianedSpikesListsList[__NeuronIndexInt])
					],
					'#kwarg':dict(
						{
							#'label':ViewedLabelStr,
							'linestyle':'',
							'marker':'|',
							'color':'black' if __NeuronIndexInt not in self.RecordingLabelVariable 
								else self.BrianedEventTraceVariable[__NeuronIndexInt][0][1]['#kwarg']['color'],
							'markersize':3 if __NeuronIndexInt not in self.RecordingLabelVariable else 5 
						},
						**self.BrianingPyplotDict
					)
				}
			),
			xrange(len(BrianedSpikesListsList))
		)


		#debug
		'''
		self.debug(
			[
				'After replace',
				('self.',self,[
					'PyplotingDrawVariable',
					#'PyplotingChartVariable'
				])
			]
		)
		'''

		#/####################/#
		# Update maybe the 
		# parent corresponding Chart Population

		#debug
		'''
		self.debug(
			[
				'Are we putting the events view in the charts population ?',
				'"Charts" not in self.BrianedParentPopulationDeriveBrianerVariable is',
				str("Charts" not in self.BrianedParentPopulationDeriveBrianerVariable.TeamDict),
				#('self.',self,[
				#		'BrianedParentPopulationDeriveBrianerVariable'
				#	])
			]
		)
		'''
		
		#Check
		if "Panels" not in self.BrianedParentPopulationDeriveBrianerVariable.TeamDict:
			return 

		#get
		BrianedRunPopulationChartDeriveManager=self.BrianedParentPopulationDeriveBrianerVariable.TeamDict[
			"Panels"
		].ManagementDict[
			"Run"
		].TeamDict[
			"Charts"
		]

		#manage
		BrianedChartDerivePyploter=BrianedRunPopulationChartDeriveManager.manage(
			self.ManagementTagStr
		).ManagedValueVariable

		#debug
		'''
		self.debug(
			[
				'We update in the parent neurongroup chart',
				'BrianedChartDerivePyploter is ',
				SYS._str(BrianedChartDerivePyploter),
			]
		)
		'''

		#Check
		if BrianedChartDerivePyploter.PyplotingChartVariable==None:

			#alias
			BrianedChartDerivePyploter.PyplotingChartVariable=self.PyplotingChartVariable
		else:

			#update
			SYS.update(
				BrianedChartDerivePyploter.PyplotingChartVariable,
				self.PyplotingChartVariable
			) 
		
		#/####################/#
		# Update maybe the 
		# parent neuron group

		#debug
		'''
		self.debug(
			[
				'Maybe we also update the view in the parent population',
				""Charts" in self.BrianedParentPopulationDeriveBrianerVariable.TeamDict is ",
				str("Charts" in self.BrianedParentPopulationDeriveBrianerVariable.TeamDict)
			]
		)
		'''

		#update the view
		map(
			lambda __KeyStr:
			BrianedChartDerivePyploter.setAttr(
				__KeyStr,
				getattr(
					self,
					__KeyStr
				)
			),
			BrianViewKeyStrsList
		)
		BrianedChartDerivePyploter.view()

		#/####################/#
		# team a Draws inside and manage a draw inside
		#

		#team
		BrianedDrawDeriveManager=BrianedChartDerivePyploter.team(
			'Draws'
		).TeamedValueVariable

		#debug
		'''
		self.debug(
			[
				'We manage a new draw',
				('self.',self,[
						'ManagementIndexInt',
						'PyplotingDrawVariable'
					])
			]
		)
		'''

		#manage
		BrianedDrawDeriveManager.manage(
			str(self.ManagementIndexInt),
			{
				'PyplotingDrawVariable':self.PyplotingDrawVariable
			}
		)

		#/####################/#
		# Update maybe the 
		# network view

		#Check
		if self.ManagementIndexInt==len(
			self.ParentDeriveTeamerVariable.ManagementDict
		)-1:

			#Check
			'''
			self.debug(
				[
					'This is the last Sample for this record',
					'We viewTraceOrEvent on this (that will call viewInteraction)',
					"self.BrianedViewTraceBool is "+str(
						self.BrianedViewTraceBool
					)
				]
			)
			'''

			#call
			self.viewTraceOrEvent()

	def viewRate(self):

		#/################/#
		# prepare the view
		#

		#get
		BrianedStateMonitorVariable=self.BrianedParentPopulationDeriveBrianerVariable.TeamDict[
			'Traces'
		].ManagementDict.getValue(
			0
		).TeamDict[
			'Samples'
		].ManagementDict.getValue(
			0
		).BrianedStateMonitorVariable

		#get
		BrianedTimeUnit=BrianedStateMonitorVariable.t.unit

		#debug
		'''
		self.debug(
			[
				'BrianedStateMonitorVariable is ',
				str(BrianedStateMonitorVariable)
			]
		)
		'''

		#import
		import brian2
		import numpy as np

		#set bins
		WindowLengthInt = int(
			self.BrianingWindowFloat*brian2.ms/self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable.clock.dt
		)

		#cumsum
		CumsumArray = np.cumsum(
			np.insert(
				self.BrianedRateMonitorVariable.rate,0,0
			)
		)

		#set
		BinRateArray = (CumsumArray[WindowLengthInt:] - CumsumArray[:-WindowLengthInt]) / WindowLengthInt
		
		#set
		self.ViewingXVariable = self.BrianedRateMonitorVariable.t[WindowLengthInt-1:]/brian2.ms
		self.ViewingYVariable = BinRateArray

		#debug
		'''
		self.debug(
			[
				('self.',self,[
						'ViewingXVariable',
						'ViewingYVariable'
					])
			]
		)
		'''
		
		#set
		self.PyplotingDrawVariable=[
			(
				'plot',
				{
					'#liarg':[
						self.ViewingXVariable,
						self.ViewingYVariable
					],
					'#kwarg':{
						'linestyle':'-',
						'linewidth':3
					}
				}


			)
		]

		#/####################/#
		# Update maybe the 
		# parent corresponding Chart Population

		#debug
		'''
		self.debug(
			[
				'Are we putting the rates view in the charts population ?',
				'"Charts" not in self.BrianedParentPopulationDeriveBrianerVariable is',
				str("Charts" not in self.BrianedParentPopulationDeriveBrianerVariable.TeamDict),
				#('self.',self,[
				#		'BrianedParentPopulationDeriveBrianerVariable'
				#	])
			]
		)
		'''
		
		#Check
		if "Panels" not in self.BrianedParentPopulationDeriveBrianerVariable.TeamDict:
			return 

		#get
		BrianedRunPopulationChartDeriveManager=self.BrianedParentPopulationDeriveBrianerVariable.TeamDict[
			"Panels"
		].ManagementDict[
			"Run"
		].TeamDict[
			"Charts"
		]

		#manage
		BrianedChartDerivePyploter=BrianedRunPopulationChartDeriveManager.manage(
			self.ManagementTagStr
		).ManagedValueVariable

		#debug
		'''
		self.debug(
			[
				'We update in the parent neurongroup chart',
				'BrianedChartDerivePyploter is ',
				SYS._str(BrianedChartDerivePyploter),
			]
		)
		'''

		#Check
		if BrianedChartDerivePyploter.PyplotingChartVariable==None:

			#alias
			BrianedChartDerivePyploter.PyplotingChartVariable=self.PyplotingChartVariable
		else:

			#update
			SYS.update(
				BrianedChartDerivePyploter.PyplotingChartVariable,
				self.PyplotingChartVariable
			) 
		
		#/####################/#
		# Update maybe the 
		# parent neuron group

		#debug
		'''
		self.debug(
			[
				'Maybe we also update the view in the parent population',
				""Charts" in self.BrianedParentPopulationDeriveBrianerVariable.TeamDict is ",
				str("Charts" in self.BrianedParentPopulationDeriveBrianerVariable.TeamDict)
			]
		)
		'''

		#update the view
		map(
			lambda __KeyStr:
			BrianedChartDerivePyploter.setAttr(
				__KeyStr,
				getattr(
					self,
					__KeyStr
				)
			),
			BrianViewKeyStrsList
		)
		BrianedChartDerivePyploter.view()

		#/####################/#
		# team a Draws inside and manage a draw inside
		#

		#team
		BrianedDrawDeriveManager=BrianedChartDerivePyploter.team(
			'Draws'
		).TeamedValueVariable

		#debug
		'''
		self.debug(
			[
				'We manage a new draw',
				('self.',self,[
						'ManagementIndexInt',
						'PyplotingDrawVariable'
					])
			]
		)
		'''

		#manage
		BrianedDrawDeriveManager.manage(
			str(self.ManagementIndexInt),
			{
				'PyplotingDrawVariable':self.PyplotingDrawVariable
			}
		)


	def mimic_simulate(self):

		#parent method
		BaseClass.simulate(self)

		#Check
		if self.BrianedNetworkVariable!=None:

			#debug
			'''
			self.debug('We start simulate in brian')
			'''

			#import
			import time

			#clock
			SimulatedTimeInt=time.clock()

			#run with the brian method
			self.BrianedNetworkVariable.run(
				self.SimulatingStopTimeFloat*self.BrianedTimeQuantityVariable
			)

			#clock
			SimulatedTimeInt=time.clock()-SimulatedTimeInt

			#debug
			'''
			self.debug(
				[
					'We stop running in brian',
					'SimulatedTimeInt is '+str(SimulatedTimeInt)+ 's'
				]
			)
			'''

		

	def recordTrace(self):

		#set
		#self.RecordedTraceFloatsArray=getattr(
		#	self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable,
		#	self.RecordKeyStr
		#)

		#base method
		BaseClass.recordTrace(self)

		#debug
		'''
		self.debug(
			[
				'We have traced, alias the init in the brian object',
				('self.',self,[
					'RecordedTraceFloatsArray',
					'RecordedInitFloatsArray'
				]),
				'self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable is ',
				str(self.BrianedParentPopulationDeriveBrianerVariable.BrianedNeurongroupVariable),
				'self.RecordedTraceFloatsArray.unit is ',
				str(self.RecordedTraceFloatsArray.unit)
			]
		)
		'''

		#set
		self.setBrianInit()

		#debug
		'''
		self.debug(
			[
				'after the set',
				('self.',self,['RecordedTraceFloatsArray'])
			]
		)
		'''

	def setBrianInit(self):

		#debug
		"""
		self.debug(
			[
				'we set brian init here',
				('self.',self,[
						'RecordedTraceFloatsArray'
					])
			]
		)
		"""
		
		#Check
		if str(self.RecordedTraceFloatsArray.unit) in ['V']:

			#import
			import brian2

			#debug
			'''
			self.debug(
				[
					"We set the initial conditions with the good dimensions",
					('self.',self,[
							'BrianingActivityQuantityStr'
						])
				]
			)
			'''

			#alias
			self.RecordedTraceFloatsArray[
				:
			]=self.RecordedInitFloatsArray*getattr(
				brian2,
				self.BrianingActivityQuantityStr
			)

		else:

			#debug
			'''
			self.debug(
				[
					'We just set direct',
					('self.',self,[
							'RecordedInitFloatsArray'
						])
				]
			)
			'''
			
			#alias
			self.RecordedTraceFloatsArray[
				:
			]=self.RecordedInitFloatsArray

	def mimic__print(self,**_KwargVariablesDict):

		#/##################/#
		# Modify the printing Variable
		#

		#Check
		if self.PrintingSelfBool:

			#/##################/#
			# Remove the brian objects that are non setted
			#

			#map
			map(
					lambda __KeyStr:
					self.forcePrint(
						[__KeyStr],
						'BrianerClass'
					)
					if getattr(self.PrintingCopyVariable,__KeyStr)!=None
					else None,
					[
						'BrianedNetworkVariable',
						'BrianedNeurongroupVariable',
						'BrianedSynapsesVariable',
						'BrianedStateMonitorVariable',
						'BrianedSpikeMonitorVariable',
						'BrianedClockVariable'
					]
				)

			#Check
			if self.PrintingCopyVariable.BrianedNeurongroupVariable!=None:

				#repr
				BaseReprStrsList=self.PrintingCopyVariable.BrianedNeurongroupVariable.__repr__(
					).split('NeuronGroup(')

				#split
				ReprStr='NeuronGroup(N='+str(self.PrintingCopyVariable.BrianedNeurongroupVariable.N
					)+', '

				#Check
				if 'threshold' in self.PrintingCopyVariable.BrianingNeurongroupDict:

					#add
					ReprStr+='thres='+self.PrintingCopyVariable.BrianingNeurongroupDict[
						'threshold'
					]+', '

				#add
				ReprStr+=BaseReprStrsList[1]

				#add the number of N
				self.PrintingCopyVariable.BrianedNeurongroupVariable=ReprStr

			#Check
			if self.PrintingCopyVariable.BrianedSynapsesVariable!=None:

				#Check
				if 'pre' in self.PrintingCopyVariable.BrianingSynapsesDict:

					#repr
					BaseReprStrsList=self.PrintingCopyVariable.BrianedSynapsesVariable.__repr__(
						).split('Synapses(')

					#Debug
					'''
					print('BaseReprStrsList is '+str(BaseReprStrsList))
					'''

					#split
					ReprStr='Synapses(pre='+str(
						self.PrintingCopyVariable.BrianingSynapsesDict['pre']
					)+', '
					ReprStr+=BaseReprStrsList[1]

					#add the pre option
					self.PrintingCopyVariable.BrianedSynapsesVariable=ReprStr

			#Check
			if self.PrintingCopyVariable.BrianedStateMonitorVariable!=None:

				#repr
				BaseReprStrsList=self.PrintingCopyVariable.BrianedStateMonitorVariable.__repr__(
					).split('StateMonitor')

				#Debug
				'''
				print('BaseReprStrsList is '+str(BaseReprStrsList))
				'''

				#split
				ReprStr='<StateMonitor, indices='+str(
					self.PrintingCopyVariable.RecordingLabelVariable
				)
				ReprStr+=BaseReprStrsList[1]

				#add the pre option
				self.PrintingCopyVariable.BrianedStateMonitorVariable=ReprStr




			#/##################/#
			# Maybe just give a pointer repr of the children
			# brian objects

			#Check
			if self.__class__.BrianingPrintBool==False or self.BrianingPrintBool==False:

				#Debug
				'''
				print('We remove the pyplot teams')
				print('self.TeamDict.keys() is ')
				print(self.TeamDict.keys())
				print('self.PrintingCopyVariable.TeamDict.keys() is ')
				print(self.PrintingCopyVariable.TeamDict.keys())
				print('')
				'''

				#map
				map(
					lambda __TeamStr:
					self.PrintingCopyVariable.TeamDict.__setitem__(
						__TeamStr,
						self.TeamDict[
								__TeamStr
							].getParenterStr()
					)
					if __TeamStr in self.TeamDict
					else None,
					['Traces','Clocks']
				)

				#Debug
				'''
				print('We remove the pyplot teams')
				print('self.TeamDict.keys() is ')
				print(self.TeamDict.keys())
				print('')
				'''



		#/##################/#
		# Call the base method
		#

		#call
		BaseClass._print(self,**_KwargVariablesDict)

#</DefineClass>

#</DefinePrint>
BrianerClass.PrintingClassSkipKeyStrsList.extend(
	[
		'BrianDebugTimeFloat',
		'BrianingNeurongroupDict',
		'BrianingSynapsesDict',
		'BrianingConnectVariable',
		'BrianingTraceDict',
		'BrianingMoniterTuple',
		'BrianingSpikesDict',
		'BrianingPyplotDict',
		'BrianingTimeQuantityStr',
		'BrianingActivityQuantityStr',
		'BrianingPyplotBool',
		'BrianingStepTimeFloat',
		'BrianingDebugVariable',
		'BrianingRecordInitBool',
		'BrianingRecordSkipKeyStrsList',
		'BrianingViewNetworkBool',
		'BrianingActivityStr',
		'BrianingViewBool', 
		'BrianingPrintBool',
		'BrianingMonitorIndexIntsList',
		'BrianingEventSelectVariable',
		'BrianingSpikeViewVariable',
		'BrianingWindowFloat',
		'BrianedEventTraceVariable',
		'BrianedTimeQuantityVariable',
		'BrianedNetworkVariable',
		'BrianedNeurongroupVariable',
		'BrianedSynapsesVariable',
		'BrianedStateMonitorVariable',
		'BrianedSpikeMonitorVariable',
		'BrianedRateMonitorVariable',
		'BrianedClockVariable',
		'BrianedRecordKeyStrsList',
		'BrianedUnitsInt',
		'BrianedTraceDeriveBrianersList',
		'BrianedSynapsesDeriveBrianersList',
		'BrianedParentDeriveBrianerStr',
		'BrianedStateDeriveBrianersList',
		'BrianedSpikeDeriveBrianersList',
		'BrianedViewTraceBool',
		'BrianedSpikesListsList',
		'BrianedTitleBool',
		'BrianedParentSingularStr',
		'BrianedParentNetworkDeriveBrianerVariable',
		'BrianedParentPopulationDeriveBrianerVariable',
		'BrianedParentInteractomeDeriveBrianerVariable',
		'BrianedParentInteractionDeriveBrianerVariable',
		'BrianedParentDeriveRecorderVariable'
	]
)
#<DefinePrint>
