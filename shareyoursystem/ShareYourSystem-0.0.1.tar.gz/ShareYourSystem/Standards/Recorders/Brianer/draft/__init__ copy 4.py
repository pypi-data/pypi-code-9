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
from ShareYourSystem.Standards.Itemizers import Pointer,Networker
from ShareYourSystem.Standards.Recorders import Recorder,Tracer
#</ImportSpecificModules>

#<DefineLocals>
class BrianersClass(Networker.NetworkerClass):pass
#</DefineLocals>

#<DefineClass>
@DecorationClass(**{
	'ClassingSwitchMethodStrsList':['brian'],
	'ClassingStructureVariable':[
			('Neurongroup','Neurongroups'),
			('Trace','Traces'),
			('Sample','Samples'),
			('Postlet','Postlets'),
			('Event','Events')
		]
})
class BrianerClass(BaseClass):
		
	def default_init(self,
			_BrianingNeurongroupDict=None,
			_BrianingSynapsesDict=None,
			_BrianingConnectVariable=None,
			_BrianingTraceDict=None,
			_BrianingMoniterTuple=None,
			_BrianingSpikesDict=None,
			_BrianingTimeDimensionVariable=None,
			_BrianedNetworkVariable=None,
			_BrianedNeurongroupVariable=None,
			_BrianedSynapsesVariable=None,
			_BrianedStateMonitorVariable=None,
			_BrianedSpikeMonitorVariable=None,
			_BrianedTraceKeyStrsList=None,
			_BrianedSynapsesDeriveBrianersList=None,
			_BrianedStateDeriveBrianersList=None,
			_BrianedSpikeDeriveBrianersList=None,
			_BrianedParentNetworkDeriveBrianerVariable=None,
			_BrianedParentNeurongroupDeriveBrianerVariable=None,
			_BrianedParentDeriveTracerVariable=None,
			**_KwargVariablesDict
		):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_brian(self):

		#debug
		self.debug(
			[
				'We brian here',
				('self.',self,['ParentedTotalSingularListDict'])
			]
		)

		#Check
		if self.ParentDeriveTeamerVariable==None or 'Neurongroups' in self.TeamDict or self.ParentDeriveTeamerVariable.TeamTagStr not in [
			'Traces','Samples'
		]:

			#/###################/#
			# Recorder level
			# structure

			#debug
			self.debug(
				[
					'It is a Network level',
					('self.',self,[
								])
				]
			)

			#/########################/#
			# Network case
			# 

			#import
			from brian2 import Network

			#structure
			self.BrianedNetworkVariable=Network()

			#/########################/#
			# make brian the neurongroups
			# 

			#structure
			self.structure(
				[
					'Neurongroups',
					'Postlets',
					'Traces',
					'Events',
					'Samples'
				],
				None
			)

			"""
			#map
			map(
				lambda __DeriveBrianer:
				__DeriveBrianer.brian(),
				self.TeamDict['Neurongroups'].ManagementDict.values()
			)
			"""


		#Check
		elif len(self.BrianingNeurongroupDict)>0:
		
			#/##################/#
			# Neurongroup case
			# adapt the BrianingNeurongroupDict and init

			#debug
			'''
			self.debug(
				[
					'It is a Neurongroup level, we set the Neurongroup',
					'We adapt the shape of BrianingNeurongroupDict',
					('self.',self,[
								'BrianingNeurongroupDict',
								'TracingKeyVariable'
							])
				]
			)
			'''

			#Check
			if 'N' not in self.BrianingNeurongroupDict:
				self.BrianingNeurongroupDict['N']=self.SimulatingUnitsInt
			else:
				self.SimulatingUnitsInt=self.BrianingNeurongroupDict['N']

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
								])
				]
			)
			'''

			#init
			self.BrianedNeurongroupVariable=NeuronGroup(
				**self.BrianingNeurongroupDict 
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
			# set the BrianedParentNeurongroupDeriveBrianerVariable
			#

			#debug
			'''
			self.debug(
				[
					'We get the parent structure',
					'self.TeamDict is ',
					SYS._str(self.TeamDict.keys())
				]
			)
			'''

			#Check
			if 'Networks' in self.TeamDict:
				if 'Brianer' in self.TeamDict['Networks'].ManagementDict:

					#debug
					'''
					self.debug(
						[
							'Brianer neurongroup is contained in a structureing brianer structure'
						]
					)
					'''

					#set
					self.BrianedParentNetworkDeriveBrianerVariable=self.TeamDict[
						'Networks'
					].ManagementDict['Brianer']

			if self.ParentDeriveTeamerVariable!=None and self.ParentDeriveTeamerVariable.TeamTagStr=='Neurongroups':
				
				#debug
				'''
				self.debug(
					[
						'Brianer neurongroup is contained in a parenting brianer structure'
					]
				)
				'''

				#set
				self.BrianedParentNetworkDeriveBrianerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

			#debug
			'''
			self.debug(
				[
					'We get the parent structure',
					('self.',self,['BrianedParentNeurongroupDeriveBrianerVariable'])
				]
			)	
			'''

			#/##################/#
			# team States first all the brian variables
			#

			#get
			self.BrianedTraceKeyStrsList=self.BrianedNeurongroupVariable.equations._equations.keys()

			#Check
			if len(self.BrianedTraceKeyStrsList)>0:

				#debug
				'''
				self.debug(
						[
							'We simulate with neurongroup',
							'adapt the initial conditions of all the brian variables',
							'so first we team Traces and put Tracers inside or get it and mapSet'
						]
					)
				'''

				#Check
				if 'Traces' not in self.TeamDict:
					BrianedDeriveTraces=self.team(
						'Traces'
					).TeamedValueVariable
				else:
					BrianedDeriveTraces=self.TeamDict[
							'Traces'
						]

				#map
				self.BrianedTraceDeriveBrianersList=map(
						lambda __ManagementKeyStr,__TraceKeyStr:
						BrianedDeriveTraces.manage(
								__ManagementKeyStr,
								{
									'TracingKeyVariable':getattr(
										self.BrianedNeurongroupVariable,
										__TraceKeyStr
									),
									'TraceKeyStr':__TraceKeyStr
								}
							).ManagedValueVariable
						if __ManagementKeyStr not in BrianedDeriveTraces.ManagementDict
						else BrianedDeriveTraces.ManagementDict[__ManagementKeyStr].mapSet(
							{
								'TracingKeyVariable':getattr(
									self.BrianedNeurongroupVariable,
									__TraceKeyStr
								),
								'TraceKeyStr':__TraceKeyStr
							}
						),
						map(
							lambda __BrianedTraceKeyStr:
							Tracer.TracerPrefixStr+__BrianedTraceKeyStr,
							self.BrianedTraceKeyStrsList
						),
						self.BrianedTraceKeyStrsList
					)

				#/##################/#
				# Case of one only pop without parent Network
				#

				#set
				BrianedNetworkBool=False

				#Check
				if 'Networks' in self.TeamDict:

					if 'Brianer' in self.TeamDict['Networks'].ManagementDict:

						#set
						BrianedNetworkBool=True

				#Check
				if self.ParentDeriveTeamerVariable!=None:

					if self.ParentDeriveTeamerVariable.TeamTagStr=='Neurongroups':

						#set
						BrianedNetworkBool=True

				#Check
				if BrianedNetworkBool==False:

					#/################/#
					# Set a structure at this place
					#

					#debug
					'''
					self.debug(
						[
							'This is just one neurongroup without parent structure'
						]
					)
					'''

					#import
					from brian2 import Network

					#structure
					self.BrianedNetworkVariable=Network()

					#/################/#
					# Maybe structure
					#

					#debug
					self.debug(
						[
							'We structure Traces,Events,Samples'
						]
					)

					#structure
					self.structure(
						[
							'Postlets',
							'Traces',
							'Events',
							'Samples'
						],
						None
					)

				else:

					#alias
					self.BrianedNetworkVariable=self.BrianedParentNetworkDeriveBrianerVariable.BrianedNetworkVariable

				#debug
				'''
				self.debug(
					[
						'Ok we know the structure ',
						('self.',self,['BrianedNetworkVariable'])
					]
				)
				'''

				#/##################/#
				# add in the net
				#

				#add
				self.BrianedNetworkVariable.add(
					self.BrianedNeurongroupVariable
				)

				#/##################/#
				# We make brian the Tracers
				#

				#debug
				'''
				self.debug(
						[
							'Make brian the tracers',
							('self.',self,['BrianedTraceDeriveBrianersList'])
						]
					)
				'''

				#map
				"""
				map(
					lambda __BrianedDeriveTracer:
					__BrianedDeriveTracer.brian(),
					self.BrianedTraceDeriveBrianersList
				)
				"""

				#debug
				'''
				self.debug(
						[
							'Ok the Tracers have brianed',
							'Now we check if it is a wrapped neurongroup into a structure or not'
						]
					)
				'''
				
			"""
			#/##################/#
			# Make brian the spikes
			#

			#debug
			self.debug(
				[
					'We make brian the Spikes'
				]
			)

			#Check
			if 'Events' in self.TeamDict:

				#map
				map(
					lambda __DeriveBrianer:
					__DeriveBrianer.brian(),
					self.TeamDict['Events'].ManagementDict.values()
				)

			#debug
			self.debug(
				[
					'We have made brian the spikes'
				]
			)
			"""

		elif self.ParentDeriveTeamerVariable.TeamTagStr=='Postlets':

			#debug
			self.debug(
				[
					'It is a Synapser level, we set the Synapser',
					('self.',self,[
								'BrianingSynapsesDict'
								]
					),
					'self.PointToVariable.BrianedNeurongroupVariable is ',
					str(self.PointToVariable.BrianedNeurongroupVariable)
				]
			)

			#/####################/#
			# Set the BrianedParentNeurongroupDeriveBrianerVariable
			#

			#get
			self.BrianedParentNeurongroupDeriveBrianerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

			#get
			self.BrianedParentNetworkDeriveBrianerVariable=self.BrianedParentNeurongroupDeriveBrianerVariable.BrianedParentNetworkDeriveBrianerVariable


			#/####################/#
			# Set the BrianedParentNeurongroupDeriveBrianerVariable
			#

			#import
			from brian2 import Synapses

			#init
			self.BrianedSynapsesVariable=Synapses(
				source=self.BrianedParentNeurongroupDeriveBrianerVariable.BrianedNeurongroupVariable,
				target=self.PointToVariable.BrianedNeurongroupVariable,
				**self.BrianingSynapsesDict
			)

			#/####################/#
			# Connect options
			#

			#connect
			if type(self.BrianingConnectVariable)==float:

				#debug
				self.debug(
					[
						'we connect with a sparsity of ',
						('self.',self,[
							'BrianingConnectVariable'
						])
					]
				)

				#connect
				self.BrianedSynapsesVariable.connect(
					True,
					p=self.BrianingConnectVariable
				)


			"""
			#/####################/#
			# Reshape the weigths
			#

			#Check
			if self.SynapsingWeigthSymbolStr!="":

				#debug
				'''
				self.debug(
					('self.',self,[
						'BrianedSynapsesVariable',
						'SynapsingWeigthSymbolStr'
						])
				)
				'''

				#connect
				self.BrianedSynapsesVariable.connect(True)

				#get
				self.SynapsedWeigthFloatsArray=getattr(
					self.BrianedSynapsesVariable,
					self.SynapsingWeigthSymbolStr
				)
				
				#set
				self.SynapsedWeigthFloatsArray[:]=np.reshape(
						self.SynapsingWeigthFloatsArray,
						self.BrianedSynapsesVariable.source.N*self.BrianedSynapsesVariable.target.N
					)

				#debug
				self.debug(
					('self.',self,[
						'SynapsedWeigthFloatsArray'
						])
				)
			"""

			#/####################/#
			# add to the structure
			#

			#add
			self.BrianedParentNetworkDeriveBrianerVariable.BrianedNetworkVariable.add(
				self.BrianedSynapsesVariable
			)


		elif self.ParentDeriveTeamerVariable.TeamTagStr=='Traces':

			#debug
			self.debug(
				[
					'It is a Tracer level, we set the Samples',
					('self.',self,[
								#'TracingKeyVariable',
								'TraceKeyStr'
								])
				]
			)

			#get
			self.BrianedParentNeurongroupDeriveBrianerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

			#/###################/#
			# Build the samples and maybe one default moniter
			#

			#Check
			if 'Samples' not in self.TeamDict:
				BrianedDeriveSamples=self.team(
					'Samples'
				).TeamedValueVariable
			else:
				BrianedDeriveSamples=self.TeamDict[
						'Samples'
					]

			#debug
			'''
			self.debug(
				[
					'Do we have to set a default moniter ?',
					'len(self.BrianedParentNeurongroupDeriveBrianerVariable.BrianedTraceKeyStrsList) is ',
					str(len(self.BrianedParentNeurongroupDeriveBrianerVariable.BrianedTraceKeyStrsList))
				]
			)
			'''

			#Check
			if len(self.BrianedParentNeurongroupDeriveBrianerVariable.BrianedTraceKeyStrsList)==1:

				#Check
				if len(BrianedDeriveSamples.ManagementDict)==0:

					BrianedDefaultMoniter=BrianedDeriveSamples.manage(
						'Default',

					).ManagedValueVariable
					BrianedDefaultMoniter.MoniteringLabelIndexIntsArray=[0] if self.BrianedParentNeurongroupDeriveBrianerVariable.BrianingNeurongroupDict[
					'N']>0 else []

			"""
			#/###################/#
			# We trace and set to the brian value
			#

			#debug
			'''
			self.debug(
				[
					'We trace and alias the init in the brian object',
					('self.',self,['TracingKeyVariable'])
				]
			)
			'''

			#trace
			self.trace()

			#debug
			'''
			self.debug(
				[
					'We have traced, alias the init in the brian object',
					('self.',self,[
						'TracedValueFloatsArray',
						'TracedInitFloatsArray'
					])
				]
			)
			'''
		
			#alias
			self.TracedValueFloatsArray[:]=self.TracedInitFloatsArray*self.TracedValueFloatsArray.unit

			#debug
			'''
			self.debug(
				[
					('self.',self,['TracedValueFloatsArray'])
				]
			)
			'''
			"""

			#

			"""
			#/###################/#
			# We make brian the Moniters
			#

			#debug
			'''
			self.debug(
				[
					'We make brian the moniters',
					'BrianedDeriveSamples.ManagementDict.keys() is ',
					str(BrianedDeriveSamples.ManagementDict.keys())
				]
			)
			'''

			#map
			map(
				lambda __DeriveMoniter:
				__DeriveMoniter.brian(),
				BrianedDeriveSamples.ManagementDict.values()
			)

			#debug
			'''
			self.debug(
				[
					'We have made brian the moniters',
				]
			)
			'''
			"""

		elif self.ParentDeriveTeamerVariable.TeamTagStr=='Samples':

			#debug
			'''
			self.debug(
				[
					'It is a State Moniter level',
					('self.',self,[
								'MoniteringLabelIndexIntsArray',
								])
				]
			)
			'''

			#/####################/#
			# Set the BrianedParentNeurongroupDeriveBrianerVariable
			#

			#get
			self.BrianedParentDeriveTracerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

			#get
			self.BrianedParentNeurongroupDeriveBrianerVariable=self.BrianedParentDeriveTracerVariable.BrianedParentNeurongroupDeriveBrianerVariable

			#get
			self.BrianedParentNetworkDeriveBrianerVariable=self.BrianedParentNeurongroupDeriveBrianerVariable.BrianedParentNetworkDeriveBrianerVariable

			#/####################/#
			# Set the brian monitor
			#
		
			#debug
			self.debug(
				[
					'We set the state monitor',
					('self.',self,[
						#'BrianedParentNeurongroupDeriveBrianerVariable'
						]),
					#'self.BrianedParentDeriveTracerVariable.TraceKeyStr is ',
					#str(self.BrianedParentDeriveTracerVariable.TraceKeyStr)
					'self.ParentedTotalManagementOrderedDict.keys() is ',
					str(self.ParentedTotalManagementOrderedDict.keys())
				]
			)

			#import
			from brian2 import StateMonitor

			#init
			self.BrianedStateMonitorVariable=StateMonitor(
					self.BrianedParentNeurongroupDeriveBrianerVariable.BrianedNeurongroupVariable,
					self.BrianedParentDeriveTracerVariable.TraceKeyStr,
					self.MoniteringLabelIndexIntsArray,
				)

			#debug
			'''
			self.debug(
				[
					'Ok we have setted the monitor',
					('self.',self,['BrianedStateMonitorVariable']),
					'Now we add to the structure',
					'self.BrianedParentNeurongroupDeriveBrianerVariable.BrianedNetworkVariable is ',
					str(self.BrianedParentNeurongroupDeriveBrianerVariable.BrianedNetworkVariable)
				]
			)
			'''

			#/####################/#
			# add to the structure
			#

			#add
			self.BrianedParentNetworkDeriveBrianerVariable.BrianedNetworkVariable.add(
				self.BrianedStateMonitorVariable
			)

		elif self.ParentDeriveTeamerVariable.TeamTagStr=='Events':

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
			# Set the BrianedParentNeurongroupDeriveBrianerVariable
			#

			#get
			self.BrianedParentNeurongroupDeriveBrianerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

			#get
			self.BrianedParentNetworkDeriveBrianerVariable=self.BrianedParentNeurongroupDeriveBrianerVariable.BrianedParentNetworkDeriveBrianerVariable


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
					self.BrianedParentNeurongroupDeriveBrianerVariable.BrianedNeurongroupVariable,
				)

			#debug
			'''
			self.debug(
				[
					'Ok we have setted the monitor',
					('self.',self,['BrianedSpikeMonitorVariable']),
					'Now we add to the structure',
					'self.BrianedParentNeurongroupDeriveBrianerVariable.BrianedNetworkVariable is ',
					str(self.BrianedParentNeurongroupDeriveBrianerVariable.BrianedNetworkVariable)
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

	def propertize_setWatchAfterParentWithParenterBool(self,_SettingValueVariable):

		#/##################/#
		# Maybe brian
		#

		#debug
		self.debug(
			[
				'We are going to parent but before',
				('self.',self,['StructuringDoStr']),
				'self.StructuringTopDeriveStructurerVariable!=self is ',
				str(self.StructuringTopDeriveStructurerVariable!=self)
			]
		)

		#Check
		if self.StructuringDoStr=='Brian' and self.StructuringTopDeriveStructurerVariable!=self:

			#record
			self.brian()

		#/##################/#
		# Call the base method
		#

		#debug
		'''
		self.debug(
			[
				'Now we call the base setParent method'
			]
		)
		'''

		#set
		BaseClass.propertize_setWatchAfterParentWithParenterBool(self,_SettingValueVariable)

	def mimic_simulate(self):

		#parent method
		BaseClass.simulate(self)

		#debug
		'''
		self.debug('We start simulate in brian')
		'''

		#Check
		if self.BrianingTimeDimensionVariable==None:

			from brian2 import ms 
			self.BrianingTimeDimensionVariable=ms

		#run with the brian method
		self.BrianedNetworkVariable.run(
			self.SimulatingStopTimeFloat*self.BrianingTimeDimensionVariable
		)

		#debug
		'''
		self.debug('We stop running in brian')
		'''

	def mimic_trace(self):

		#base method
		BaseClass.trace(self)

		#debug
		'''
		self.debug(
			[
				'We have traced, alias the init in the brian object',
				('self.',self,[
					'TracedValueFloatsArray',
					'TracedInitFloatsArray'
				])
			]
		)
		'''

		#alias
		self.TracedValueFloatsArray[:]=self.TracedInitFloatsArray*self.TracedValueFloatsArray.unit

		#debug
		'''
		self.debug(
			[
				('self.',self,['TracedValueFloatsArray'])
			]
		)
		'''

	def mimic_draw(self):

		


		"""
		self.DrawingSetVariable={
				'|A':{
					'-Axes':[
						('ManagingBeforeSetVariable',
						{
							'FiguringShapeIntsTuple':(5,15),
							'#copy:FiguringDrawVariable':
							[
								(
									'#axes',
									[
										('set_xticks',{
													'#liarg:#map@get':[
														">>SYS.set(SYS,'TimeTicksArray',SYS.getTickFloatsArray([0.,self.PredisensingRunTimeFloat],4)).TimeTicksArray"
													]	
										}),
										('set_xticklabels',{
											'#liarg:#map@get':[
												">>map(lambda __Float:'$%.0f$'%__Float,SYS.TimeTicksArray)"
											]
										}),
										('set_xlim',{
											'#liarg:#map@get':[0.,'>>self.PredisensingRunTimeFloat']
										})
									]
								)
							]
						}),
						('|Sensor',{
							'-Plots':{
								'#map@set':map(
									lambda __IntsTuple:
									(
										'|'+str(__IntsTuple[0]),
										{
											'FiguringDrawVariable':
											[
												('#plot',
													{
														'#liarg:#map@get':[
															'PredisensedTimeTraceFloatsArray',
															'>>self.PredisensedInputCurrentTraceFloatsArray.__getitem__('+str(__IntsTuple[1])+')'
														],
														'#kwarg':{
															'label':'$\\tau_{D}c_{'+str(__IntsTuple[1])+'}$',
															'linestyle':'-',
															'color':self.PredisenseCommandColorTuplesList[__IntsTuple[0]]
														}
												}),
												('#plot',
													{
														'#liarg:#map@get':[
															'PredisensedTimeTraceFloatsArray',
															'>>self.PredisensedSensorTraceFloatsArray['+str(__IntsTuple[1])+',:]'
														],
														'#kwarg':{
															'color':self.PredisenseSensorColorTuplesList[__IntsTuple[0]],
															'label':'$x_{'+str(__IntsTuple[1])+'}$',
															'linewidth':3,
															'linestyle':'-'
														}
												})
											]
										}
									),
									enumerate(self.PredisensingMonitorIntsList)
								)	
							},
							'FiguringDrawVariable.extend':
							[[
								(
									'#axes',
									[
										('set_ylabel','$\\tau_{D}c(t),\ x(t)$'),
										('set_ylim',{'#liarg:#map@get':[
											"".join([
												">>SYS.set(SYS,'SensorLimFloatsArray',",
												"[min(-0.1,self.PredisensedSensorTraceFloatsArray.min()),1.5*self.PredisensingClampFloat*self.PredictingConstantTimeFloat]",
												').SensorLimFloatsArray'
											])]
										}),
										('set_yticks',{
											'#liarg:#map@get':[
												"".join([
													">>SYS.set(SYS,'SensorTickFloatsArray',",
													"map(lambda __Float:float('%.2f'%__Float),",
													"SYS.getTickFloatsArray(",
													"SYS.SensorLimFloatsArray,3",
													"))).SensorTickFloatsArray"
												])
											]
										}),
										('set_yticklabels',{
											'#liarg:#map@get':[
												"".join([
													">>SYS.set(SYS,'SensorTickStrsArray',",
													"map(lambda __Float:'$'+str(__Float)+'$',",
													"SYS.SensorTickFloatsArray)).SensorTickStrsArray"
													])
											]
										}),
										('tick_params',{
											'#kwarg':{
												'length':10,
												'width':5,
												'which':'major'
											}
										}),
										('tick_params',{
											'#kwarg':{
												'length':5,
												'width':2,
												'which':'minor'
											}
										}),
										('xaxis.set_ticks_position',
											{
												'#liarg':['bottom']
											}
										),
										('yaxis.set_ticks_position',
											{
												'#liarg':['left']
											}
										),
										('legend',{
											'#liarg':[],
											'#kwarg':{
												'fontsize':10,
												'shadow':True,
												'fancybox':True,
												'ncol':max(1,len(self.PredisensingMonitorIntsList)/2),
												'loc':2,
												'bbox_to_anchor':(1.05, 1)
											}
										})
									]
								)
							]]
						})
					]
				}				
			}
		"""

#</DefineClass>

#<DefineLocals>

#set
BrianerClass.TeamingClassesDict.update(
	{
		'Neurongroups':BrianersClass,
		'Postlets':BrianersClass,
		'Traces':BrianersClass,
		'Events':BrianersClass,
		'Samples':BrianersClass
	}
)
BrianersClass.ManagingValueClass=BrianerClass

#</DefineLocals>


#</DefinePrint>
BrianerClass.PrintingClassSkipKeyStrsList.extend(
	[
		'BrianingNeurongroupDict',
		'BrianingSynapsesDict',
		'BrianingConnectVariable',
		'BrianingTraceDict',
		'BrianingMoniterTuple',
		'BrianingSpikesDict',
		'BrianingTimeDimensionVariable',
		#'BrianedNetworkVariable',
		#'BrianedNeurongroupVariable',
		#'BrianedSynapsesVariable',
		#'BrianedStateMonitorVariable',
		#'BrianedSpikeMonitorVariable',
		'BrianedTraceKeyStrsList',
		'BrianedSynapsesDeriveBrianersList',
		'BrianedStateDeriveBrianersList',
		'BrianedSpikeDeriveBrianersList',
		'BrianedParentNetworkDeriveBrianerVariable',
		'BrianedParentNeurongroupDeriveBrianerVariable',
		'BrianedParentDeriveTracerVariable'
	]
)
#<DefinePrint>
