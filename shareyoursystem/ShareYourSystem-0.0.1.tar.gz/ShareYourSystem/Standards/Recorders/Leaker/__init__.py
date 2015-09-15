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

# Second-order statistics
def correlogram(T1,T2,width,bin,T=None):
	'''
		Returns a cross-correlogram with lag in [-width,width] and given bin size.
		T is the total duration (optional) and should be greater than the duration of T1 and T2.
		The result is in Hz (rate of coincidences in each bin).
		
		N.B.: units are discarded.
		TODO: optimise?
	'''
	#import
	import numpy as np 
	# Remove units
	width=float(width)
	T1=np.array(T1)
	T2=np.array(T2)
	i=0
	j=0
	n=int(np.ceil(width/bin)) # Histogram length
	l=[]
	for t in T1:
		while i<len(T2) and T2[i]<t-width: # other possibility use searchsorted
			i+=1
		while j<len(T2) and T2[j]<t+width:
			j+=1
		l.extend(T2[i:j]-t)
	H,_=np.histogram(l,bins=np.arange(2*n+1)*bin-n*bin)

	# Divide by time to get rate
	if T is None:
		T=max(T1[-1],T2[-1])-min(T1[0],T2[0])
	# Windowing function (triangle)
	W=np.zeros(2*n)
	W[:n]=T-bin*np.arange(n-1,-1,-1)
	W[n:]=T-bin*np.arange(n)
	return H/W
#</DefineLocals>

#<DefineClass>
@DecorationClass(**{
	'ClassingSwitchMethodStrsList':['leak'],
	'ClassingStructureVariable':[
			('Population','Populations'),
			('Trace','Traces'),
			('Sample','Samples'),
			('Event','Events'),
			('Rate','Rates'),
			('Interactome','Interactomes'),
			('Interaction','Interactions'),
			('Input','Inputs')
		]
})
class LeakerClass(BaseClass):
		
	def default_init(self,
			_LeakingUnitsInt=0,
			_LeakingTimeVariable='#scalar:10.*ms',
			_LeakingWeightVariable=None,
			_LeakingQuantityStr='mV',
			_LeakingSymbolPrefixStr="",
			_LeakingInteractionStr="Rate",
			_LeakingVariableStr="",
			_LeakingTransferVariable=None,
			_LeakingThresholdVariable=None,
			_LeakingResetVariable=None,
			_LeakingRefractoryVariable=None,
			_LeakingRecordBool=False,
			_LeakingNoiseStdVariable=None,
			_LeakingDelayVariable=None,
			_LeakingDelayCustomBool=False,
			_LeakingDelayPrepostBool=False,
			_LeakingPlasticRuleVariable=None,
			_LeakingPlasticPreBool=True,
			_LeakingGlobalBool=False,
			_LeakingTotalBool=False,
			_LeakingThresholdMethodStr="",
			_LeakingEigenBool=False,
			_LeakingMaxBool=False,
			_LeakingMinPhaseTimeVariable=None,
			_LeakingMaxPhasesInt=2,
			_LeakingAutoCorrelationBool=False,
			_LeakedStepTimeFloat=0.1,
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
			_LeakedInteractionWeightFloat=0.,
			_LeakedParentSingularStr="",
			_LeakedParentNetworkDeriveLeakerVariable=None,
			_LeakedParentPopulationDeriveLeakerVariable=None,
			_LeakedParentInteractomeDeriveLeakerVariable=None,
			_LeakedTimedArrayVariable=None,
			_LeakedVariableStr="",
			_LeakedDelayTimeFloatsArray=None,
			_LeakedDelayTotalIntVariable=None,
			_LeakedDelayValueFloatVariable=None,
			_LeakedDelayCursorIntVariable=None,
			_LeakedDelayActivityFloatsArray=None,
			_LeakedDelayBufferFloatsArray=None,
			_LeakedDelaySymbolStr="",
			_LeakedMinFloat=0.,
			_LeakedMaxFloat=0.,
			_LeakedMeanGlobalFloatsArray=None,
			_LeakedStdGlobalFloatsArray=None,
			_LeakedSimulationStateMonitorVariable=None,
			_LeakedThresholdMethod=None,
			_LeakedRandomFunction=None,
			_LeakedInputKeyStrsList=None,
			_LeakedBrianWeightFloatsArray=None,
			_LeakedPhaseList=None,
			_LeakedMeanStateMonitorVariable=None,
			_LeakedVarStateMonitorVariable=None,
			_LeakedMaxSpikeMonitorVariable=None,
			_LeakedMaxStateMonitorVariable=None,
			_LeakedGlobalSynapsesVariable=None,
			_LeakedWeightPhaseList=None,
			**_KwargVariablesDict
		):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	#/##################/#
	# leak methods
	#

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
					'Rates',
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
		# Determine the parent
		#

		#set
		if self.ParentDeriveTeamerVariable!=None:
			self.LeakedParentNetworkDeriveLeakerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable
		else:
			self.LeakedParentNetworkDeriveLeakerVariable=self

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
							'LeakingWeightVariable'
						])
				]
			)
			'''

			#type
			LeakedType=type(self.LeakingWeightVariable)

			#Check
			if LeakedType==str:

				#Check
				if self.LeakingWeightVariable in ['0','0.0']:

					#set the right
					self.LeakedModelStr+='('

				else:

					#set the right
					self.LeakedModelStr+='(-'+self.LeakingWeightVariable+'*'+self.LeakedSymbolStr

			elif LeakedType in [list]:

				#link
				self.LeakedModelStr='''
					mu : 1
				'''+self.LeakedModelStr

			elif self.LeakingWeightVariable!=None:

				#set the right
				self.LeakedModelStr+='(-'+str(
					self.LeakingWeightVariable
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
				if self.LeakingTransferVariable!=None:

					#Check
					if self.LeakedModelStr[-1]!='(':
						self.LeakedModelStr+='+'

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
								('+'+self.LeakedCurrentStr)
								if self.LeakedCurrentStr[0]!='-'
								else self.LeakedCurrentStr
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
							'We add directly the leaked current',
							('self.',self,[
									'LeakedCurrentStr',
									'LeakedModelStr'
								])
						]
					)
					'''

					#Check
					if self.LeakedCurrentStr[0]!='-' and self.LeakedModelStr[-1]!='(':

						#Check
						self.LeakedModelStr+='+'

					#Check
					self.LeakedModelStr+=self.LeakedCurrentStr

			#debug
			"""
			self.debug(
				[
					'We divide by the time',
					('self.',self,[
						'LeakedClampStr',
						'LeakedModelStr',
						'LeakingNoiseStdVariable'
					])
				]
			)
			"""

			#Check
			if self.LeakingNoiseStdVariable!=None:

				#Check
				self.LeakedModelStr+='+'

				#Check
				if type(self.LeakingNoiseStdVariable)==str:

					#debug
					self.debug(
						[
							"We add",
							('self.',self,['LeakingNoiseStdVariable'])
						]
					)

					#add
					self.LeakedModelStr+=self.LeakingNoiseStdVariable

				else:

					#str
					self.LeakedModelStr+=str(
						self.LeakingNoiseStdVariable
					)+'*'+str(self.LeakedQuantityVariable)

				#add
				self.LeakedModelStr+='*sqrt('+self.LeakedTimeSymbolStr+')*xi'

			#set
			self.LeakedModelStr+=')'

			#set the right denominator
			if self.LeakedClampStr in ["Scalar","Variable"]:

				#add
				self.LeakedModelStr+='/('+self.LeakedTimeSymbolStr+')'

			#set the dimension
			self.LeakedModelStr+=' : '+self.LeakedDimensionStr

		#/##################/#
		# Init the Neurongroup dict
		#

		#init
		BrianingNeurongroupDict={
				}

		#/##################/#
		# Look for a refractory period 
		#

		#type
		LeakedRefractoryType=type(self.LeakingRefractoryVariable)

		#Check
		if LeakedRefractoryType!=None.__class__:

			#import
			import numpy as np

			#Check
			if LeakedRefractoryType in [float,np.float64]:

				#import
				import brian2

				#set
				BrianingNeurongroupDict[
					'refractory'
				]=self.LeakingRefractoryVariable*getattr(
					brian2,
					self.BrianingTimeQuantityStr
				)
			
			#/###############/#
			# Add in the model
			#

			#debug
			'''
			self.debug(
				[
					('self.',self,[
							'LeakedModelStr'
						])
				]
			)
			'''

			#add
			self.LeakedModelStr+=' (unless refractory)'

		#add
		self.LeakedModelStr+="\n"

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
		LeakedRecordDeriveLeaker=LeakedTracesDeriveManager.getManager(
				Recorder.RecordPrefixStr+self.LeakedSymbolStr
			)

		#set
		LeakedRecordDeriveLeaker.NumscipyingStdFloat=0.001
		LeakedSamplesDeriveLeaker=LeakedRecordDeriveLeaker.getTeamer(
				'Samples'
			)
		LeakedDefaultDeriveLeaker=LeakedSamplesDeriveLeaker.getManager(
				'Default'
			)

		#/##################/#
		# Look for what to monitor
		#

		#debug
		'''
		self.debug(
			[
				('self.',self,[
					'RecordingLabelVariable'
				])
			]
		)
		'''

		#Check
		if self.RecordingLabelVariable!=None:

			#copy
			LeakedDefaultDeriveLeaker.RecordingLabelVariable=self.RecordingLabelVariable[:]

		else:

			#debug
			'''
			self.debug(
				[
					'Check the monitor indexes',
					('self.',self,[
							'BrianingMonitorIndexIntsList',
							'LeakingUnitsInt'
						])
				]
			)
			'''
			
			#Check
			if self.BrianingMonitorIndexIntsList==None or len(self.BrianingMonitorIndexIntsList
				)==0:

				#set
				self.BrianingMonitorIndexIntsList=[0]
				
			elif len(
				self.BrianingMonitorIndexIntsList
			)>self.LeakingUnitsInt:

				#set
				self.BrianingMonitorIndexIntsList=self.BrianingMonitorIndexIntsList[:self.LeakingUnitsInt]

			#set
			LeakedDefaultDeriveLeaker.RecordingLabelVariable=self.BrianingMonitorIndexIntsList[:]

		#/##################/#
		# Look for a Max pick 
		#

		#Check
		if self.LeakingMaxBool:

			#debug
			'''
			self.debug(
				[
					'We build a variable that tracks the max events'
				]
			)
			'''

			#add
			self.LeakedModelStr+=self.LeakedSymbolStr+'_diff : '+self.LeakedDimensionStr+'\n'
			self.LeakedModelStr+=self.LeakedSymbolStr+'_diff_max : '+self.LeakedDimensionStr+'\n'

			#join
			LeakedDiffStr='\n'.join(
					map(
					lambda __IndexInt:
					self.LeakedSymbolStr+'_differenciater_'+str(
						__IndexInt
					)+' : '+self.LeakedDimensionStr,
					xrange(1,-1,-1)
				)
			)+'\n'
			self.LeakedModelStr+=LeakedDiffStr

			#debug
			'''
			self.debug(
				[
					'In the end of max model',
					('self.',self,[
							'LeakedModelStr'
						])
				]
			)
			'''

			'''
			LeakedPhaseNeuronGroup=brian2.NeuronGroup(
				self.LeakingUnitsInt,
				'\n'.join(
					[
						'r_diff : '+self.LeakedDimensionStr,
						'detect = (r_diff<0)'
					]
				),
				threshold='detect==1'
			)
			'''

			#define the threshold
			BrianingNeurongroupDict[
				'threshold'
			]=self.LeakedSymbolStr+'_diff_max<0*mV'

			#append
			self.LeakedRecordSkipStrsList.extend(
				map(
					lambda __KeyStr:
					self.LeakedSymbolStr+__KeyStr,
					[
						'_diff',
						'_diff_max',
						'_differenciater_0',
						'_differenciater_1'
					]
				)
			)

		#/##################/#
		# Look for a Threshold 
		#

		#debug
		'''
		self.debug(
			[
				'Look for a threshold',
				('self.',self,[
					'LeakingThresholdVariable',
					'LeakingThresholdMethodStr'
				])
			]
		)
		'''

		#Check
		if type(self.LeakingThresholdVariable)!=None.__class__:

			#type
			LeakedType=type(self.LeakingThresholdVariable)

			#debug
			'''
			self.debug(
				[
					"There is a threshold",
					"LeakedType is "+str(LeakedType)
				]
			)
			'''
			
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

					#import
					import brian2

					#get
					Dimension=getattr(brian2,self.LeakingQuantityStr)

					#set
					self.BrianingSpikeViewVariable=[(
						float("".join(BrianingNeurongroupDict['threshold'].split('*')[0].split('>')[1:]))
					)*Dimension,-10.*Dimension]

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



					#Check
					if LeakedType in [float,np.float64]:

						#set
						BrianedThresholdFloat=self.LeakingThresholdVariable

					else:

						#set
						BrianedThresholdFloat=np.array(
							self.LeakingThresholdVariable
						).min()

					#import
					import brian2

					#get
					Dimension=getattr(brian2,self.LeakingQuantityStr)

					#set
					self.BrianingSpikeViewVariable=[
						BrianedThresholdFloat*Dimension,
						-10.*Dimension
					]

					#append
					if self.LeakedRecordSkipStrsList==None:
						self.LeakedRecordSkipStrsList=['Threshold']
					else:
						self.LeakedRecordSkipStrsList.append(
							'Threshold'
						)

				
						
		#Check
		if self.LeakingThresholdMethodStr!="":
	
			#import
			from brian2 import network_operation
			import numpy as np

			#randint
			self.LeakedRandomFunction=np.random.randint

			#define
			@network_operation(when='after_thresholds')
			def ThresholdFunction():

				#get
				getattr(
					self,
					self.LeakingThresholdMethodStr
				)(
				)

			#alias
			self.LeakedThresholdMethod=ThresholdFunction

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
		if type(self.LeakingResetVariable)!=None.__class__:

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

		#/##################/#
		# Is there a global variable to compute
		#

		#Check
		if self.LeakingGlobalBool and self.LeakingTotalBool==False:

			#debug
			'''
			self.debug(
				[
					'We compute a global statistical variables',
					('self.',self,[
							'LeakedModelStr'
						])
				]
			)
			'''

			LeakedMeanGlobalSymbolStr='Mean_'+self.LeakedSymbolStr
			LeakedVarGlobalSymbolStr='Var_'+self.LeakedSymbolStr

			#add
			self.LeakedModelStr+=LeakedMeanGlobalSymbolStr +' : '+self.LeakedDimensionStr

			#add
			self.LeakedModelStr+='\n'+LeakedVarGlobalSymbolStr +' : 1'

			#debug
			'''
			self.debug(
				[
					'In the end',
					('self.',self,[
							'LeakedModelStr'
						])
				]
			)
			'''

			#append
			self.LeakedRecordSkipStrsList.extend(
				[
					LeakedMeanGlobalSymbolStr,
					LeakedVarGlobalSymbolStr
				]
			)

			#debug
			"""
			self.debug(
				[
					"We have extended the LeakedRecordSkipStrsList",
					('self.',self,[
							"LeakedRecordSkipStrsList"
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

		#/###################/#
		# Specify maybe records of the events and rates
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
					"Default_Events"
				)

			#debug
			'''
			self.debug(
				[
					'We add a record of the rates'
				]
			)
			'''
			
			#get
			self.getTeamer(
					"Rates"
				).getManager(
					"Default_Rates"
			)

	def leakTrace(self):

		#/#################/#
		# Determine the parent
		#

		#set
		self.LeakedParentPopulationDeriveLeakerVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

		#set
		self.LeakedParentNetworkDeriveLeakerVariable=self.LeakedParentPopulationDeriveLeakerVariable.LeakedParentNetworkDeriveLeakerVariable

		#debug
		'''
		self.debug(
			[
				'We have determined the parent',
				('self.',self,[
						'LeakedParentPopulationDeriveLeakerVariable',
						'LeakedParentNetworkDeriveLeakerVariable'
					])
			]
		)
		'''

		#/#################/#
		# If this a trace with a threshold
		# then center the random pick around it

		#debug
		'''
		self.debug(
			[
				"Do we care to init under the threshold ?",
				"self.LeakedParentPopulationDeriveLeakerVariable.BrianedNeurongroupVariable is ",
				str(self.LeakedParentPopulationDeriveLeakerVariable.BrianedNeurongroupVariable)
			]
		)
		'''

		#Check
		#if hasattr(
		#	self.LeakedParentPopulationDeriveLeakerVariable.BrianedNeurongroupVariable,
		#	'Threshold'
		#):
		if type(
			self.LeakedParentPopulationDeriveLeakerVariable.LeakingThresholdVariable
		) != None.__class__ :

			#debug
			'''
			self.debug(
				[
					"Yes, we care to init under the threshold ?"
				]
			)
			'''

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
				LeakedThresholdType=type(
					self.LeakedParentPopulationDeriveLeakerVariable.LeakingThresholdVariable
				)

				#import
				import numpy as np

				#Check
				if LeakedThresholdType in [float,np.float64]:
					self.LeakedMaxFloat=self.LeakedParentPopulationDeriveLeakerVariable.LeakingThresholdVariable
				elif LeakedThresholdType ==str:
					self.LeakedMaxFloat=float(
						"".join(
							self.LeakedParentPopulationDeriveLeakerVariable.LeakingThresholdVariable.split('>')[1:]
							).split("*")[0])
				else:
					self.LeakedMaxFloat=self.LeakedParentPopulationDeriveLeakerVariable.LeakingThresholdVariable.min()

				#debug
				'''
				self.debug(
					[
						('self.',self,['LeakedMaxFloat'])
					]
				)
				'''

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

		#Check
		if self.ManagementTagStr.startswith("Delta"):

			#debug
			self.debug(
				[
					'Special case of a Delta record variable'
				]
			)

			#set
			self.BrianingRecordInitBool=False

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

		#type
		LeakedWeightType=type(self.LeakingWeightVariable)

		#debug
		'''
		self.debug(
			[
				"The type of the input is specified ?",
				"LeakedWeightType is "+str(LeakedWeightType)
			]
		)
		'''

		#Check
		if LeakedWeightType!=None.__class__:

			#init
			self.LeakedClampStr="Variable"

			#Check
			if LeakedWeightType==str:

				#Check
				if self.LeakingWeightVariable.startswith(
					LeakScalarPrefixStr
				):

					#set
					self.LeakedClampStr="Scalar"

					#set
					self.LeakedSymbolStr=SYS.deprefix(
						self.LeakingWeightVariable,
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

				elif self.LeakingWeightVariable.startswith(
					LeakEquationPrefixStr
				):

					#set
					self.LeakedClampStr='Equation'

					#set
					self.LeakedOperationStr=SYS.deprefix(
						self.LeakingWeightVariable,
						LeakEquationPrefixStr
					)

					#setOperation
					self.setOperation()

				elif self.LeakingWeightVariable.startswith(
					LeakCustomPrefixStr
				):

					#set
					self.LeakedClampStr='Custom'

					#set
					self.LeakedOperationStr=SYS.deprefix(
						self.LeakingWeightVariable,
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
			elif LeakedWeightType in [list,tuple]:

				#Check
				if type(self.LeakingWeightVariable[0])==str:

					#Check
					if self.LeakingWeightVariable[0].startswith(LeakNetworkPrefixStr[:-1]):

						#debug
						'''
						self.debug(
							[
								'It is a network operation',
								('self.',self,[
										'LeakingWeightVariable'
									])
							]
						)
						'''

						#set
						self.LeakedClampStr='Network'

						#set
						self.LeakedOperationStr=SYS.deprefix(
							self.LeakingWeightVariable[0],
							LeakNetworkPrefixStr
						)

						#setOperation
						self.setOperation()

					elif self.LeakingWeightVariable[0].startswith(
						LeakCustomPrefixStr[:-1]
					):

						#debug
						'''
						self.debug(
							[
								'It is a map of different input variables',
								('self.',self,[
										'LeakingWeightVariable'
									])
							]
						)
						'''

						#set
						self.LeakedClampStr='Custom'	

						#set
						self.LeakedOperationStr=SYS.deprefix(
							self.LeakingWeightVariable[0],
							LeakCustomPrefixStr[:-1]
						)

						#debug
						'''
						self.debug(
							[
								('self.',self,[
										'LeakedOperationStr'
									])
							]
						)
						'''

						#Check
						if self.LeakedOperationStr!="" and self.LeakedOperationStr[0]==':':
							self.LeakedOperationStr=self.LeakedOperationStr[1:]+':'

						#join
						self.LeakedOperationStr+="+".join(
								map(
									lambda __IndexInt,__CustomOperationStr:
									__CustomOperationStr+'*(i=='+str(
										__IndexInt
									)+')',
									xrange(len(self.LeakingWeightVariable[1])),
									self.LeakingWeightVariable[1]
								)
							)

						#setOperation
						self.setOperation()

			#debug
			'''
			self.debug(
				[
					'Is it a variable',
					('self.',self,[
							'LeakedClampStr'
						])
				]
			)
			'''

			#Check
			if self.LeakedClampStr=="Variable":

				#debug
				'''
				self.debug(
					[
						'It is a variable',
						('self.',self,[
								'LeakedSymbolStr',
								'LeakingRecordBool'
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
							'we skip record this input',
							('self.',self,['LeakedSymbolStr'])
						]
					)
					'''

					#append
					if self.LeakedParentPopulationDeriveLeakerVariable.LeakedRecordSkipStrsList==None:

						#add
						self.LeakedParentPopulationDeriveLeakerVariable.LeakedRecordSkipStrsList=[
							self.LeakedSymbolStr
						]

					else:

						#append
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
							'LeakedSymbolStr',
							'LeakingRecordBool'
						])
				]
			)
			'''

		#debug
		'''
		self.debug(
			[
				'Should we have to take care of a record later',
				('self.',self,[
						'LeakedClampStr'
					])
			]
		)
		'''

		#Check
		if self.LeakedClampStr not in ["Scalar","Variable"]:

			#/###############/#
			# Make sure that trace of input is before trace trace of activity
			# Look for a RecordingVariable
			#

			#get
			LeakedTraceDeriveLeaker=self.LeakedParentPopulationDeriveLeakerVariable.getTeamer(
					"Traces"
				).manage(
					Recorder.RecordPrefixStr+self.LeakedSymbolStr,
					_IndexInt=0
				).ManagedValueVariable

			#Check
			if self.RecordingLabelVariable!=None:

				#debug
				'''
				self.debug(
					[
						'In the input we set the recording label variable to the corresponding trace sample',
						('self.',self,['RecordingLabelVariable'])
					]
				)
				'''

				#set
				LeakedTraceDeriveLeaker.getTeamer(
					"Samples"
				).getManager(
					"Default"
				).setAttr(
					"RecordingLabelVariable",
					self.RecordingLabelVariable
				)


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
						'LeakingWeightVariable'
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
				'What is LeakingWeightVariable',
				('self.',self,[
						'LeakingWeightVariable'
					])
			]
		)
		'''
		
		#Check
		if type(self.LeakingWeightVariable)==None.__class__:

			#set
			self.LeakingWeightVariable='#scalar:0.'

			#debug
			'''
			self.debug(
				[
					'We set a default J equal to scalar 0',
					('self.',self,[
							'LeakingWeightVariable'
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
					'LeakingWeightVariable'
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

		#debug
		'''
		self.debug(
			[
				"Look if it is a scalar interaction",
				('self.',self,[
						'LeakingWeightVariable'
					])
			]
		)
		'''

		#Check
		if type(self.LeakingWeightVariable)==str:

			#Check
			if self.LeakingWeightVariable.startswith(
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

		#debug
		'''
		self.debug(
			[
				"Do we have to record this interaction variable",
				('self.',self,['LeakedClampStr'])
			]
		)
		'''

		#Check
		if self.LeakedClampStr=="Variable":

			#debug
			'''
			self.debug(
				[
					'It is a variable',
					('self.',self,[
							'LeakedSymbolStr',
							'LeakingRecordBool'
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

			else:

				#get
				self.ConnectedToVariable.getTeamer(
					'Traces'
				).getManager(
					self.LeakedSymbolStr,
					_IndexInt=0
				).getTeamer(
					'Samples'
				).getManager(
					'Default'
				)

				#debug
				"""
				self.debug(
					[
						'we build the trace already',
						'self.ConnectedToVariable.TeamDict["Traces"].ManagementDict.keys() is ',
						str(self.ConnectedToVariable.TeamDict["Traces"].ManagementDict.keys())
					]
				)	
				"""

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
					'LeakedClampStr',
					'LeakingWeightVariable'
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
				LeakedInteractionWeightStr=SYS.deprefix(
					self.LeakingWeightVariable,
					LeakScalarPrefixStr
				)

				#set
				self.LeakedInteractionWeightFloat=float(LeakedInteractionWeightStr)

				#add
				self.LeakedModelStr+="="+LeakedInteractionWeightStr+'*'+self.LeakedVariableStr+"_pre"

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
			"""
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
			"""

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

				#set
				self.LeakedStepTimeFloat=self.LeakedParentNetworkDeriveLeakerVariable.BrianingStepTimeFloat

				#debug
				'''
				self.debug(
					[
						'We are going to model delays in the rate',
						('self.',self,[
								'LeakedModelStr',
								'LeakingDelayVariable',
								'LeakedStepTimeFloat'
							]),
						#'self.LeakedParentPopulationDeriveLeakerVariable.LeakingTimeVariable is',
						#str(self.LeakedParentPopulationDeriveLeakerVariable.LeakingTimeVariable)
					]
				)
				'''

				#import
				import numpy as np

				#Check
				if LeakedDelayType in [float,np.float64]:

					#import
					from brian import ms

					#array
					self.LeakedDelayTimeFloatsArray=np.array(
						[self.LeakingDelayVariable]
					)

					#divide and put that in ms...(rough)
					self.LeakedDelayTotalIntVariable=(int)(
							self.LeakingDelayVariable/
								self.LeakedStepTimeFloat
						)

				elif LeakedDelayType in [list,np.ndarray]:

					#transpose
					self.LeakingDelayVariable=np.array(
						self.LeakingDelayVariable
					).T

					#divide and put that in ms...(rough)
					self.LeakedDelayTotalIntVariable=map(
						lambda __Variable:
						(int)
						(
							max(self.LeakedStepTimeFloat,__Variable)/
								self.LeakedStepTimeFloat
						) if type(__Variable) in [float,np.float64]
						else map(
							lambda ____Variable:
							(int)
							(
								max(self.LeakedStepTimeFloat,____Variable)/
									self.LeakedStepTimeFloat
							),
							__Variable
						),
						self.LeakingDelayVariable
					)

					#debug
					'''
					self.debug(
						[
							'In the end',
							('self.',self,[
									'LeakedDelayTotalIntVariable'
								])
						]
					)
					'''


				#get
				LeakedPopulationSymbolStr=self.LeakedParentPopulationDeriveLeakerVariable.LeakedSymbolStr

				#Check
				if self.LeakingDelayCustomBool:

					#debug
					'''
					self.debug(
						[
							'We build delays with a custom operation',
							'only if there is one unique delay'
						]
					)
					'''

					#join
					LeakedDefinitionStr="\n".join(
						map(
								lambda __IndexInt:
								LeakedPopulationSymbolStr+"_delayer_"+str(
									__IndexInt
								)+" : "+self.LeakedParentPopulationDeriveLeakerVariable.LeakedDimensionStr,
								xrange(
									self.LeakedDelayTotalIntVariable[0]
								)
							)
					)

					#replace
					self.LeakedModelStr=self.LeakedModelStr.replace(
						LeakedPopulationSymbolStr+'_pre',
						LeakedPopulationSymbolStr+"_delayer_"+str(
							self.LeakedDelayTotalIntVariable[0]-1
						)
					)

					#add
					self.LeakedModelStr+=LeakedDefinitionStr

				else:

					#debug
					'''
					self.debug(
						[
							'We build delays with a network operation'
						]
					)
					'''

					#set
					self.LeakedDelaySymbolStr=LeakedPopulationSymbolStr+"_delayer"

					#Check
					if type(self.LeakedDelayTotalIntVariable)!=int:

						#add
						self.LeakedModelStr=self.LeakedDelaySymbolStr+' : '+self.LeakedParentPopulationDeriveLeakerVariable.LeakedDimensionStr+'\n'+self.LeakedModelStr

						#replace
						self.LeakedModelStr=self.LeakedModelStr.replace(
							LeakedPopulationSymbolStr+'_pre',
							self.LeakedDelaySymbolStr
						)

					else:

						#just add in the parent pop
						self.LeakedParentPopulationDeriveLeakerVariable.LeakedModelStr+=self.LeakedDelaySymbolStr+' : '+self.LeakedParentPopulationDeriveLeakerVariable.LeakedDimensionStr+'\n'

						#replace
						self.LeakedModelStr=self.LeakedModelStr.replace(
							LeakedPopulationSymbolStr+'_pre',
							self.LeakedDelaySymbolStr+'_pre'
						)

						#append
						if self.LeakedParentPopulationDeriveLeakerVariable.LeakedRecordSkipStrsList==None:

							self.LeakedParentPopulationDeriveLeakerVariable.LeakedRecordSkipStrsList=[
								self.LeakedDelaySymbolStr
							]
						else:	

							self.LeakedParentPopulationDeriveLeakerVariable.LeakedRecordSkipStrsList.append(
								self.LeakedDelaySymbolStr
							)

					#debug
					'''
					self.debug(
						[
							'In the end',
							('self.',self,[
									'LeakedModelStr'
								]),
							'self.LeakedParentPopulationDeriveLeakerVariable.LeakedModelStr is '+self.LeakedParentPopulationDeriveLeakerVariable.LeakedModelStr
						]
					)
					'''

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

		#debug
		'''
		self.debug(
			[
				('self.',self,[
						'LeakingPlasticRuleVariable',
						'LeakingInteractionStr'
					])
			]
		)
		'''

		#Check
		if self.LeakingPlasticRuleVariable!=None:

			#Check
			if self.LeakingInteractionStr=="Rate":
				
				#debug
				'''
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
				'''

				#set
				#BrianedModelStr='beta : 1'
				#BrianedModelStr+='\nlambda : 1'
				#BrianedModelStr+='\nd'+self.LeakingSymbolPrefixStr+'/dt=beta*('
				#BrianedModelStr+='I_Command_post-lambda*'+self.LeakingSymbolPrefixStr+')'	

				#add
				self.LeakedModelStr+="\n"+self.LeakingPlasticRuleVariable

				#debug
				'''
				self.debug(
					[
						'after update of the model',
						('self.',self,[
								'LeakedModelStr'
							])
					]
				)
				'''

		else:

			#debug
			'''
			self.debug(
				[
					"We add in the not record",
					('self.',self,[
							'LeakedRecordSkipStrsList',
							'BrianingRecordSkipKeyStrsList'
						])
				]
			)
			'''

			#Check
			if self.BrianingRecordSkipKeyStrsList==None:
				self.BrianingRecordSkipKeyStrsList=[self.LeakingSymbolPrefixStr]
			else:
				self.BrianingRecordSkipKeyStrsList.append(self.LeakingSymbolPrefixStr)


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

			#add
			self.BrianingSynapsesDict['pre']=self.ConnectedToVariable.LeakedSymbolStr+'_post+='+self.LeakingSymbolPrefixStr+'*'+str(
				self.LeakedParentPopulationDeriveLeakerVariable.LeakedQuantityVariable
			)

			#debug
			'''
			self.debug(
				[
					'It is a spike interaction add int the BrianingSynapsesDict pre',
					'self.ConnectedToVariable.LeakedSymbolStr is ',
					self.ConnectedToVariable.LeakedSymbolStr,
					('self.',self,[
							'LeakedModelStr'
						]),
					"self.BrianingSynapsesDict['pre'] is "+str(
						self.BrianingSynapsesDict['pre']
					)
				]
			)
			'''

			#/##################/#
			# Look for plasticity in the spike
			#

			#Check
			if self.LeakingPlasticRuleVariable!=None:

				#debug
				'''
				self.debug(
					[
						'It is a spike model',
						('self.',self,[
								'LeakedSymbolStr',
								'LeakingPlasticRuleVariable'
							])
					]
				)
				'''
				
				#add
				if self.LeakingPlasticPreBool:

					#/##############/#
					# BE CAREFUL the update needs to be before the update of the voltage for autapses
					#

					#set
					self.BrianingSynapsesDict['pre']=self.LeakingPlasticRuleVariable+'\n'+self.BrianingSynapsesDict['pre']
				else:

					#set
					self.BrianingSynapsesDict['post']+='\n'+self.LeakingPlasticRuleVariable

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


	#/##################/#
	# brian methods
	#

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
		# Look at Max
		#

		#Check
		if self.LeakingMaxBool:

			#/###################/#
			# Define the custom operation
			#

			#set
			BrianedCustomStr=self.LeakedSymbolStr+'_diff=('+self.LeakedSymbolStr+'-'+self.LeakedSymbolStr+'_differenciater_0) \n'
			BrianedCustomStr+=self.LeakedSymbolStr+'_diff_max=(1./'+self.LeakedDimensionStr+')*('+self.LeakedSymbolStr+'_differenciater_0-'+self.LeakedSymbolStr+'_differenciater_1)*'+self.LeakedSymbolStr+'_diff*('+self.LeakedSymbolStr+'_diff<0.*mV'+') \n'

			#join
			BrianedCustomStr+='\n'.join(
					map(
					lambda __IndexInt:
					self.LeakedSymbolStr+'_differenciater_'+str(
						__IndexInt
					)+'='+self.LeakedSymbolStr+'_differenciater_'+str(
						__IndexInt-1
					)
					if __IndexInt>0
					else self.LeakedSymbolStr+'_differenciater_'+str(
						__IndexInt
					)+'='+self.LeakedSymbolStr,
					xrange(2,-1,-1)
				)
			)

			#debug
			'''
			self.debug(
				[
					'picking the max',
					'BrianedCustomStr is '+str(BrianedCustomStr)
				]
			)
			'''

			#custom
			BrianedCustomOperation=self.BrianedNeurongroupVariable.custom_operation(
				BrianedCustomStr
			)

			#add
			self.BrianedParentNetworkDeriveBrianerVariable.BrianedNetworkVariable.add(
				BrianedCustomOperation
			)
			
			#/###################/#
			# Define the way to record
			#

			#import
			from brian2 import SpikeMonitor

			#init
			self.LeakedMaxSpikeMonitorVariable=SpikeMonitor(
				self.BrianedNeurongroupVariable
			)

			#add
			self.BrianedParentNetworkDeriveBrianerVariable.BrianedNetworkVariable.add(
				self.LeakedMaxSpikeMonitorVariable
			)
	
			"""
			#import
			from brian2 import StateMonitor

			#init
			self.LeakedMaxStateMonitorVariable=StateMonitor(
				self.BrianedNeurongroupVariable,
				self.LeakedSymbolStr+'_diff_max',
				True
			)

			#add
			self.BrianedParentNetworkDeriveBrianerVariable.BrianedNetworkVariable.add(
				self.LeakedMaxStateMonitorVariable
			)
			"""


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

			#Check
			if 'Threshold' not in self.BrianingRecordSkipKeyStrsList:

				#set in the Threshold Trace to not record
				self.TeamDict[
					'Traces'
				].ManagementDict[
					Recorder.RecordPrefixStr+'Threshold'
				].BrianingRecordInitBool=False

		#Check
		if self.LeakedThresholdMethod!=None:

			#add
			self.LeakedParentNetworkDeriveLeakerVariable.BrianedNetworkVariable.add(
				self.LeakedThresholdMethod
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


		#/################/#
		# Look for computing a global variable
		#

		#Check
		if self.LeakingGlobalBool and self.LeakingTotalBool==False:

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
			'''
			self.debug(
				[
					'LeakedGlobalModelStr is ',
					LeakedGlobalModelStr
				]
			)	
			'''

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
				self.TeamDict[
					'Inputs'
				].ManagementDict.values()
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
					#'self.TeamDict["Inputs"].ManagementDict.keys() is ',
					#str(self.TeamDict["Inputs"].ManagementDict.keys()),
					'BrianedTracesManager.ManagementDict.keys() is ',
					str(BrianedTracesManager.ManagementDict.keys())

				]	
			)
			'''

			#map
			self.LeakedInputKeyStrsList=map(
					lambda __DeriveLeaker:
					Recorder.RecordPrefixStr+__DeriveLeaker.LeakedSymbolStr,
					SYS._filter(
						lambda __DeriveLeaker:
						__DeriveLeaker.LeakedClampStr not in ["","Scalar"],
						self.TeamDict['Inputs'].ManagementDict.values()
					)
				)

			#debug
			'''
			self.debug(
				[

					('self.',self,['LeakedInputKeyStrsList'])
				]
			)
			'''

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
		if self.LeakingWeightVariable!=None:

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

				#import
				import numpy as np

				#set
				setattr(
					self.LeakedParentPopulationDeriveLeakerVariable.BrianedNeurongroupVariable,
					self.LeakedSymbolStr,
					#self.LeakingWeightVariable*Variable.unit
					self.LeakingWeightVariable*self.LeakedParentPopulationDeriveLeakerVariable.LeakedQuantityVariable
					if type(self.LeakingWeightVariable) in [
						np.float64,float
					] else (
						self.LeakingWeightVariable*self.LeakedParentPopulationDeriveLeakerVariable.LeakedQuantityVariable
						if type(self.LeakingWeightVariable[0]) in [
							np.float64,float
						] else self.LeakingWeightVariable
					)
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
					self.LeakingWeightVariable,
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

				#get
				BrianedInputQuantity=getattr(
						BrianedNeurongroupVariable,
						self.LeakedSymbolStr
					)

				if self.LeakedClockStr=="":

					@network_operation
					def updateInput():

						#get set
						BrianedInputQuantity[:]=self.LeakingWeightVariable[1](
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
						BrianedInputQuantity[:]=self.LeakingWeightVariable[1](
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
						'LeakingWeightVariable'
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
		self.LeakedBrianWeightFloatsArray=None

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
					('self.',self,['LeakedInteractionWeightFloat'])
				]
			)
			'''

			#Check
			if self.LeakedInteractionWeightFloat!=0.:

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
			BrianedInteractionType=type(self.LeakingWeightVariable)

			#debug
			'''
			self.debug(
				[
					'We have to set the connect variable',
					('self.',self,[
						'LeakingWeightVariable'
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
								'LeakingWeightVariable'
							])
					]
				)
				'''

				#Check
				if self.LeakingWeightVariable!=0.:

					#debug
					'''
					self.debug(
						[
							'We are going to connect this Variable for each index',
							('self.',self,[
									'LeakingWeightVariable'
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
					)[:]=self.LeakingWeightVariable
					

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
					self.LeakedBrianWeightFloatsArray=self.NumscipiedValueFloatsArray

				else:

					#shape
					self.LeakedBrianWeightFloatsArray=getShapeArray(
						np.array(self.LeakingWeightVariable),
						BrianedRowsInt,
						BrianedColsInt
					)

				#/###############/#
				# Shape correctly
				#

				#reshape
				LeakedBrianReshapeWeightFloatsArray=np.reshape(
					np.array(
						self.LeakedBrianWeightFloatsArray
					).T,
					BrianedRowsInt*BrianedColsInt
				)

				#debug
				'''
				self.debug(
					[
						'It is an already defined array',
						('self.',self,[
								'LeakingWeightVariable'
							]),
						'self.BrianedSynapsesVariable.source.N is '+str(self.BrianedSynapsesVariable.source.N),
						'self.BrianedSynapsesVariable.target.N is '+str(self.BrianedSynapsesVariable.target.N),
						'LeakedBrianReshapeWeightFloatsArray is '+str(LeakedBrianReshapeWeightFloatsArray)
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
				BrianedInteractionArray[:]=LeakedBrianReshapeWeightFloatsArray

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
					self.BrianedSynapsesVariable.pre.delay[
						:
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

				#Check
				if self.LeakingDelayCustomBool:

					#debug
					'''
					self.debug(
						[
							'This is a rate model',
							'add the delay as a custom opera

							tion',
							('self.',self,[
									'LeakedDelayTotalIntVariable'
								])
						]
					)
					'''

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
								xrange(self.LeakedDelayTotalIntVariable[0]-1,0,-1)
							)+[
							LeakedSymbolStr+"_delayer_0="+LeakedSymbolStr+'_pre'
						]
					)
					
					#debug
					'''
					self.debug(
						[
							'BrianedDelayStr is '+str(BrianedDelayStr)
						]
					)
					'''

					#custom
					self.LeakedParentNetworkDeriveLeakerVariable.BrianedNetworkVariable.add(
						self.BrianedSynapsesVariable.custom_operation(
							BrianedDelayStr,
							dt=self.BrianedSynapsesVariable.clock.dt
						)
					)

				else:

					#debug
					'''
					self.debug(
						[
							'This is a rate model',
							'add the delay as a network operation',
							('self.',self,[
									'LeakedDelayTotalIntVariable',
								])
						]
					)
					'''
					
					#get
					self.LeakedDelayActivityFloatsArray=getattr(
						self.LeakedParentPopulationDeriveLeakerVariable.BrianedNeurongroupVariable,
						self.LeakedParentPopulationDeriveLeakerVariable.LeakedSymbolStr
					)

					#import
					from brian2 import network_operation

					#/###############/#
					# Define the delay monitor
					#

					#init
					'''
					BrianedRecentStateMonitor=StateMonitor(
						self.LeakedParentPopulationDeriveLeakerVariable.BrianedNeurongroupVariable,
						self.LeakedParentPopulationDeriveLeakerVariable.LeakedSymbolStr,
						duration=self.LeakedDelayTimeFloatsArray.max(
							)*self.LeakedParentNetworkDeriveLeakerVariable.BrianedTimeQuantityVariable,
						record=True
					)
					'''

					#Check
					if type(self.LeakedDelayTotalIntVariable)!=int:

						#get
						self.LeakedDelayBufferFloatsArray=getattr(
							self.BrianedSynapsesVariable,
							self.LeakedDelaySymbolStr
						)


						#debug
						'''
						self.debug(
							[
								'Build eakedDelayBoxFloatsArray that is not the same size everywhere'
							]
						)
						'''

						#map
						self.LeakedDelayValueFloatVariable=map(
							lambda __LeakedDelayTimeVariable:
							[
								[0. for ____IndexInt in xrange(__LeakedDelayTimeVariable)]
								for __IndexInt in xrange(
									self.LeakedParentPopulationDeriveLeakerVariable.LeakingUnitsInt
								)
							]
							if type(__LeakedDelayTimeVariable)==int
							else
							map(
								lambda __LeakedDelayTimeInt:
								[0.]*__LeakedDelayTimeInt,
								__LeakedDelayTimeVariable
							),
							self.LeakedDelayTotalIntVariable
						)

						#map
						self.LeakedDelayCursorIntVariable=map(
							lambda __LeakedDelayTimeVariable:
							0
							if type(__LeakedDelayTimeVariable)==int
							else
							map(
								lambda __LeakedDelayTimeInt:
								0,
								__LeakedDelayTimeVariable
							),
							self.LeakedDelayTotalIntVariable
						)

						self.LeakedDelayCursorIntVariable=np.array(
							self.LeakedDelayCursorIntVariable
						)

						#array
						self.LeakedDelayValueFloatVariable=np.array(
							self.LeakedDelayValueFloatVariable
						)
					
					else:

						#debug
						'''
						self.debug(
							[
								'Build LeakedDelayValueFloatVariable homogeneous',
								('self.',self,[
										'LeakedDelayTotalIntVariable'
									])
							]
						)
						'''

						#get
						self.LeakedDelayBufferFloatsArray=getattr(
							self.LeakedParentPopulationDeriveLeakerVariable.BrianedNeurongroupVariable,
							self.LeakedDelaySymbolStr
						)

						#set
						self.LeakedDelayValueFloatVariable=[
							self.LeakedDelayBufferFloatsArray
							for __IndexInt in xrange(self.LeakedDelayTotalIntVariable)
						]

						#map
						self.LeakedDelayCursorIntVariable=0

						#debug
						'''
						self.debug(
							[
								('self.',self,[
										'LeakedDelayValueFloatVariable'
									]
								)
							]
						)
						'''

					
					#debug
					'''
					self.debug(
						[
							'We have defined the recent delay monitor',
							('self.',self,[
									'LeakedDelayValueFloatVariable',
									'LeakedDelayCursorIntVariable'
								])
						]
					)
					'''

					#get
					'''
					LeakedDelayBufferFloatsArray=getattr(
						BrianedRecentStateMonitor,
						self.LeakedDelaySymbolStr
					)
					'''

					#/###############/#
					# Define the delay method
					#

					#Check
					if self.LeakingDelayPrepostBool:

						#debug
						'''
						self.debug(
							[
								'We define delay with maybe same presynaptic delay rows',
								('self.',self,[
										'LeakedDelayTotalIntVariable',
										'LeakedDelayCursorIntVariable',
										'LeakedDelayValueFloatVariable'
									])
							]
						)
						'''

						#define
						@network_operation(
							clock=self.BrianedSynapsesVariable.clock
						)
						def setDelay():

							#/###############/#
							# Determine the indexes
							#

							#debug
							'''
							self.debug(
								[
									'We set delay here with maybe same presynaptic delay rows',
									('self.',self,[
											'LeakedDelayTotalIntVariable',
											'LeakedDelayCursorIntVariable',
											'LeakedDelayValueFloatVariable'
										])
								]
							)
							'''

							#map
							map(
								lambda __RowIndexInt,__LeakedDelayCursorIntVariable,__LeakedDelayTimeIntVariable:
									self.setRowDelay(
										__RowIndexInt,__LeakedDelayCursorIntVariable,__LeakedDelayTimeIntVariable
									)
								if type(__LeakedDelayTimeIntVariable)==int
								else map(
									lambda __ColIndexInt,__LeakedDelayBoxInt,__LeakedDelayTimeInt:
									self.setColRowDelay(
										__RowIndexInt,__ColIndexInt,__LeakedDelayBoxInt,__LeakedDelayTimeInt
									),
									xrange(len(__LeakedDelayTimeIntVariable)),
									__LeakedDelayCursorIntVariable,
									__LeakedDelayTimeIntVariable,
								),
								xrange(len(self.LeakedDelayCursorIntVariable)),
								self.LeakedDelayCursorIntVariable,
								self.LeakedDelayTotalIntVariable
							)

							#debug
							'''
							self.debug(
								[
									'Now',
									('self.',self,[
											'LeakedDelayCursorIntVariable',
											'LeakedDelayValueFloatVariable'
										]),
									#'DelayTimeFloat is '+str(DelayTimeFloat)
								]
							)
							'''

						
					#Check
					elif type(self.LeakedDelayCursorIntVariable)==int:

						#debug
						'''
						self.debug(
							[
								'We set define delay here with one unique value',
								('self.',self,[
										'LeakedDelayTotalIntVariable',
										'LeakedDelayCursorIntVariable',
										'LeakedDelayValueFloatVariable'
									])
							]
						)
						'''

						#define
						@network_operation(
							clock=self.BrianedSynapsesVariable.clock
						)
						def setDelay():

							#/###############/#
							# Determine the indexes
							#

							#debug
							'''
							self.debug(
								[
									'We set unique delay here',
									('self.',self,[
											'LeakedDelayTotalIntVariable',
											'LeakedDelayCursorIntVariable',
											'LeakedDelayValueFloatVariable',
											'LeakedDelayActivityFloatsArray'
										])
								]
							)
							'''
							
							#/#############/#
							# "update" in the box the last recorded value
							#

							#set
							self.LeakedDelayValueFloatVariable[
								self.LeakedDelayCursorIntVariable
							]=self.LeakedDelayActivityFloatsArray[:]

							#set
							self.LeakedDelayCursorIntVariable=self.LeakedDelayCursorIntVariable+1 if self.LeakedDelayCursorIntVariable<self.LeakedDelayTotalIntVariable-1 else 0

							#/#############/#
							# set the new delay variable
							# 

							#debug
							'''
							self.debug(
								[
									'We set in the delayer at ',
									('self.',self,[
											'LeakedDelayActivityFloatsArray',
											'LeakedDelayValueFloatVariable',
											'LeakedDelayBufferFloatsArray'
										])
								]
							)
							'''

							#set
							self.LeakedDelayBufferFloatsArray[
								:
							]=self.LeakedDelayValueFloatVariable[self.LeakedDelayCursorIntVariable][:]


							#debug
							'''
							self.debug(
								[
									'Now',
									('self.',self,[
											'LeakedDelayCursorIntVariable',
											'LeakedDelayValueFloatVariable'
										]),
									#'DelayTimeFloat is '+str(DelayTimeFloat)
								]
							)
							'''

					else:

						#define
						@network_operation(
							clock=self.BrianedSynapsesVariable.clock
						)
						def setDelay():

							#/###############/#
							# Determine the indexes
							#

							#debug
							'''
							self.debug(
								[
									'We set delay here',
									('self.',self,[
											'LeakedDelayTotalIntVariable',
											'LeakedDelayCursorIntVariable',
											'LeakedDelayValueFloatVariable'
										])
								]
							)
							'''

							#map
							map(
								lambda __RowIndexInt,__LeakedDelayCursorIntVariable,__LeakedDelayTimeIntVariable:
								map(
									lambda __ColIndexInt,__LeakedDelayBoxInt,__LeakedDelayTimeInt:
									self.setRowColDelay(
										__RowIndexInt,__ColIndexInt,__LeakedDelayBoxInt,__LeakedDelayTimeInt
									),
									xrange(len(__LeakedDelayTimeIntVariable)),
									__LeakedDelayCursorIntVariable,
									__LeakedDelayTimeIntVariable,
								),
								xrange(len(self.LeakedDelayCursorIntVariable)),
								self.LeakedDelayCursorIntVariable,
								self.LeakedDelayTotalIntVariable
							)

							#debug
							'''
							self.debug(
								[
									'Now',
									('self.',self,[
											'LeakedDelayCursorIntVariable',
											'LeakedDelayValueFloatVariable'
										]),
									#'DelayTimeFloat is '+str(DelayTimeFloat)
								]
							)
							'''

					#add
					self.LeakedParentNetworkDeriveLeakerVariable.BrianedNetworkVariable.add(
						setDelay
					)	

		#/####################/#
		# Do we compute some things on the connectivity
		#

		#Check
		if type(self.LeakedBrianWeightFloatsArray)!=None.__class__:

			#Check
			if self.LeakingEigenBool:

				#set
				self.NumscipyingValueVariable=self.LeakedBrianWeightFloatsArray
				self.NumscipyingEigenvalueBool=True

				#debug
				'''
				self.debug(
					[
						'We are going to look to the Eigen of the connectivity'
					]
				)
				'''

				#numscipy
				self.numscipy()

				#debug
				'''
				self.debug(
					[
						'The eigen of the connectivity gives',
						('self.',self,[
							'NumscipiedCenterFloat',
							'NumscipiedWidthFloat',
							'NumscipiedHeightFloat'
						])
					]	
				)
				'''


	def setRowDelay(self,_RowIndexInt,_LeakedDelayBoxInt,_LeakedDelayTimeInt):

		#debug
		'''
		self.debug(
			[
				'we set delay row here',
				"[_RowIndexInt,_LeakedDelayBoxInt,_LeakedDelayTimeInt]) is",
				str([_RowIndexInt,_LeakedDelayBoxInt,_LeakedDelayTimeInt])
			]
		)
		'''

		#/#############/#
		# "update" in the box the last recorded value
		#

		#get
		LeakedDelayFloatsArray=self.LeakedDelayValueFloatVariable[
					_RowIndexInt,
					:
				]

		#map
		map(
			lambda __IntAndArrayTuple:
			__IntAndArrayTuple[1].__setitem__(
				_LeakedDelayBoxInt,
				self.LeakedDelayActivityFloatsArray[__IntAndArrayTuple[0]]
			),
			enumerate(
				LeakedDelayFloatsArray
			)
		)

		#/#############/#
		# move forward
		# 

		#set
		LeakedDelayNewBoxInt=_LeakedDelayBoxInt+1 if _LeakedDelayBoxInt<_LeakedDelayTimeInt-1 else 0

		#set
		self.LeakedDelayCursorIntVariable.__setitem__(
			_RowIndexInt,
			LeakedDelayNewBoxInt
		)

		#/#############/#
		# set the new delay variable
		# 

		#debug
		'''
		self.debug(
			[
				'We set the new value in the synapses',
				('self.',self,[
						'LeakedDelayBufferFloatsArray'
					])
			]
		)
		'''

		#set
		'''
		self.LeakedDelayBufferFloatsArray[:,_RowIndexInt]=map(
			lambda __IntAndArrayTuple:
			__IntAndArrayTuple[1].__setitem__(
				LeakedDelayNewBoxInt,
				self.LeakedDelayBufferFloatsArray[__IntAndArrayTuple[0]]
			),
			enumerate(
				LeakedDelayFloatsArray
			)
		)
		'''

		#debug
		'''
		self.debug(
			[
				'We have setted row delay here',
				'LeakedDelayNewBoxInt is '+str(LeakedDelayNewBoxInt),
				('self.',self,[
						'LeakedDelayValueFloatVariable'
					])
			]
		)
		'''

	def setColRowDelay(self,_RowIndexInt,_ColIndexInt,_LeakedDelayBoxInt,_LeakedDelayTimeInt):

		#debug
		'''
		self.debug(
			[
				'we set delay col row here',
				"[_RowIndexInt,_ColIndexInt,_LeakedDelayBoxInt,_LeakedDelayTimeInt]) is",
				str([_RowIndexInt,_ColIndexInt,_LeakedDelayBoxInt,_LeakedDelayTimeInt]),
				('self.',self,[
						'LeakedDelayValueFloatVariable'
					])
			]
		)
		'''

		#/#############/#
		# "update" in the box the last recorded value
		#

		#set
		LeakedDelayFloatsArray=self.LeakedDelayValueFloatVariable.__getitem__(
				(
					_RowIndexInt,
					_ColIndexInt
				)
			)

		#set
		LeakedDelayFloatsArray.__setitem__(
				_LeakedDelayBoxInt,
				self.LeakedDelayActivityFloatsArray[_ColIndexInt]
			)

		#/#############/#
		# move forward
		# 

		#set
		LeakedDelayNewBoxInt=_LeakedDelayBoxInt+1 if _LeakedDelayBoxInt<_LeakedDelayTimeInt-1 else 0

		#set
		self.LeakedDelayCursorIntVariable.__getitem__(
				_RowIndexInt
			).__setitem__(
				_ColIndexInt,
				LeakedDelayNewBoxInt
		)

		#/#############/#
		# set the new delay variable
		# 

		#debug
		'''
		self.debug(
			[
				'We set in the delayer at ',
				str(
		_ColIndexInt*self.LeakedParentPopulationDeriveLeakerVariable.LeakingUnitsInt+_RowIndexInt),
				('self.',self,[
						'LeakedDelayBufferFloatsArray'
					])
			]
		)
		'''

		#set
		self.LeakedDelayBufferFloatsArray[
			_RowIndexInt*self.LeakedParentPopulationDeriveLeakerVariable.LeakingUnitsInt+_ColIndexInt
		]=LeakedDelayFloatsArray[LeakedDelayNewBoxInt]

		#debug
		'''
		self.debug(
			[
				'We have setted row col delay here',
				'LeakedDelayNewBoxInt is '+str(LeakedDelayNewBoxInt),
				('self.',self,[
						'LeakedDelayValueFloatVariable'
					])
			]
		)
		'''


	def setRowColDelay(self,_RowIndexInt,_ColIndexInt,_LeakedDelayBoxInt,_LeakedDelayTimeInt):

		#debug
		'''
		self.debug(
			[
				'we set delay row col here',
				"[_RowIndexInt,_ColIndexInt,_LeakedDelayBoxInt,_LeakedDelayTimeInt]) is",
				str([_RowIndexInt,_ColIndexInt,_LeakedDelayBoxInt,_LeakedDelayTimeInt]),
				('self.',self,[
						'LeakedDelayValueFloatVariable'
					])
			]
		)
		'''

		#/#############/#
		# "update" in the box the last recorded value
		#

		#set
		LeakedDelayFloatsArray=self.LeakedDelayValueFloatVariable.__getitem__(
				(
					_RowIndexInt,
					_ColIndexInt
				)
			)

		#set
		LeakedDelayFloatsArray.__setitem__(
				_LeakedDelayBoxInt,
				self.LeakedDelayActivityFloatsArray[_ColIndexInt]
			)

		#/#############/#
		# move forward
		# 

		#set
		LeakedDelayNewBoxInt=_LeakedDelayBoxInt+1 if _LeakedDelayBoxInt<_LeakedDelayTimeInt-1 else 0

		#set
		self.LeakedDelayCursorIntVariable.__getitem__(
				_RowIndexInt
			).__setitem__(
				_ColIndexInt,
				LeakedDelayNewBoxInt
		)

		#/#############/#
		# set the new delay variable
		# 

		#debug
		'''
		self.debug(
			[
				'We set in the delayer at ',
				str(
		_ColIndexInt*self.LeakedParentPopulationDeriveLeakerVariable.LeakingUnitsInt+_RowIndexInt),
				('self.',self,[
						'LeakedDelayBufferFloatsArray'
					])
			]
		)
		'''

		#set
		self.LeakedDelayBufferFloatsArray[
			_RowIndexInt*self.LeakedParentPopulationDeriveLeakerVariable.LeakingUnitsInt+_ColIndexInt
		]=LeakedDelayFloatsArray[LeakedDelayNewBoxInt]

		#debug
		'''
		self.debug(
			[
				'We have setted row col delay here',
				'LeakedDelayNewBoxInt is '+str(LeakedDelayNewBoxInt),
				('self.',self,[
						'LeakedDelayValueFloatVariable'
					])
			]
		)
		'''



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

		#set
		LeakedWordStr=self.ManagementTagStr.split(
			Recorder.RecordPrefixStr
		)[1] if len(Recorder.RecordPrefixStr)>0 else self.ManagementTagStr

		#Check
		if LeakedWordStr in self.LeakedParentPopulationDeriveLeakerVariable.LeakedRecordSkipStrsList or (
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
			if BrianedParentInteractionDeriveBrianerVariable.LeakingPlasticRuleVariable!=None and type(
				BrianedParentInteractionDeriveBrianerVariable.LeakingWeightVariable
			)!=None.__class__:

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
		#if hasattr(
		#	self.LeakedParentPopulationDeriveLeakerVariable.BrianedNeurongroupVariable,
		#	'Threshold'
		#):
		if 'threshold' in self.LeakedParentPopulationDeriveLeakerVariable.BrianingNeurongroupDict:

			#Check
			if self.RecordKeyStr==self.LeakedParentPopulationDeriveLeakerVariable.LeakedSymbolStr:

				#min value
				self.LeakedMinFloat=self.RecordedInitFloatsArray.min()

				#set
				LeakedShiftFloat=-0.05*abs(self.LeakedMaxFloat)

				#set
				LeakedSubthresholdFloat=self.LeakedMaxFloat+LeakedShiftFloat

				#debug
				'''
				self.debug(
					[
						'We init under the thresholds',
						('self.',self,[
								'ManagementTagStr',
								'RecordKeyStr',
								'RecordedInitFloatsArray',
								'LeakedMaxFloat'
							]),
						'LeakedSubthresholdFloat is '+str(
							LeakedSubthresholdFloat
						)
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
						self.RecordedInitFloatsArray.__getitem__(
							__IndexInt
						)+LeakedShiftFloat
					)
					if self.RecordedInitFloatsArray[
						__IndexInt
					]>LeakedSubthresholdFloat
					else None,
					xrange(
						len(self.RecordedInitFloatsArray)
					)
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
				
				#call
				self.setBrianInit()

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
							self.LeakedParentPopulationDeriveLeakerVariable.BrianingMonitorIndexIntsList
						):

						#alias
						BrianedDefaultDeriveLeaker.RecordingLabelVariable=self.LeakedParentPopulationDeriveLeakerVariable.BrianingMonitorIndexIntsList

					else:

						#debug
						'''
						self.debug(
							[
								'WARNING : size is not good',
								'self.LeakedParentPopulationDeriveLeakerVariable.BrianedNeurongroupVariable.N is',
								str(self.LeakedParentPopulationDeriveLeakerVariable.BrianedNeurongroupVariable.N),
								'self.LeakedParentPopulationDeriveLeakerVariable.BrianingMonitorIndexIntsList is ',
								str(self.LeakedParentPopulationDeriveLeakerVariable.BrianingMonitorIndexIntsList)
							]
						)
						'''
						
						#alias
						BrianedDefaultDeriveLeaker.RecordingLabelVariable=[0]


	def brianSample(self):

		#/################/#
		# Determine parent
		#

		#set
		self.BrianedParentDeriveRecorderVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

		#set
		self.LeakedParentPopulationDeriveLeakerVariable=self.BrianedParentDeriveRecorderVariable.LeakedParentPopulationDeriveLeakerVariable


		#/################/#
		# If there is a global computation
		#

		#debug
		'''
		self.debug(
			[
				'We brian sample leak here',
				#'self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable is',
				#str(self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable),
				('self.',self,[
					'ParentTagStr'
				]),
				'self.LeakedParentPopulationDeriveLeakerVariable.LeakedInputKeyStrsList is ',
				str(self.LeakedParentPopulationDeriveLeakerVariable.LeakedInputKeyStrsList)
			]
		)
		'''

		#Check
		if self.LeakedParentPopulationDeriveLeakerVariable.LeakingTotalBool:

			#debug
			'''
			self.debug(
				[
					'We are going to record all the units to do stats on it'
				]
			)
			'''

			#set
			self.BrianingMonitorIndexIntsList=range(
				self.LeakedParentPopulationDeriveLeakerVariable.LeakingUnitsInt
			)

		elif self.BrianedParentDeriveRecorderVariable.ManagementTagStr in self.LeakedParentPopulationDeriveLeakerVariable.LeakedInputKeyStrsList:

			'''
			#set
			self.BrianingMonitorIndexIntsList=self.LeakedParentPopulationDeriveLeakerVariable.TeamDict[
				'Inputs'
			].ManagementDict[
				"".join(
					self.BrianedParentDeriveRecorderVariable.ManagementTagStr.split('_')[1:]
				)
			].RecordingLabelVariable
			'''
			
			#alias
			#self.RecordingLabelVariable=self.BrianingMonitorIndexIntsList

			#debug
			'''
			self.debug(
				[
					'This is an input trace',
					('self.',self,[
							'BrianingMonitorIndexIntsList'
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
					'BrianingMonitorIndexIntsList'
				])
			]
		)
		'''
		
		#/################/#
		# Call the base
		#

		#brianSample
		BaseClass.brianSample(self)
		
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

			#set
			self.LeakedCurrentStr=_CurrentStr

		elif _CurrentStr[0]=='-':

			#add
			self.LeakedCurrentStr+=_CurrentStr

		else:

			#add
			self.LeakedCurrentStr+='+'+_CurrentStr

		#debug
		'''
		self.debug(
			[
				'In the end',
				('self.',self,[
					'LeakedCurrentStr'
				])
			]
		)
		'''

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

	#/##################/#
	# simulate methods
	#

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
		'''
		self.debug(
			[
				'We simulate population here'
			]
		)
		'''
		
		#Check
		if self.LeakingTotalBool or self.LeakingGlobalBool:

			#debug
			'''
			self.debug(
				[
					'We compute the global properties'
				]
			)
			'''
			
			#get
			self.LeakedSimulationStateMonitorVariable=self.TeamDict[
					'Traces'
				].ManagementDict[
					Recorder.RecordPrefixStr+self.LeakedSymbolStr
				].TeamDict[
					'Samples'
				].ManagementDict[
					'Default'
				].BrianedStateMonitorVariable

			#Check
			if self.LeakingTotalBool:

				#import 
				import numpy as np

				#numscipy
				self.NumscipyingValueVariable=np.array(
					getattr(
						self.LeakedSimulationStateMonitorVariable,
						self.LeakedSymbolStr
					)
				)
				self.NumscipyingSampleFloatsArray=np.array(
					self.LeakedSimulationStateMonitorVariable.t
				)
				self.NumscipyingGlobalBool=self.LeakingTotalBool
				self.numscipy()

		#Check
		if self.LeakingMaxBool:

			#debug
			'''
			self.debug(
				[
					'We plot the max',
					('self.',self,[
							'LeakedMaxSpikeMonitorVariable',
							'LeakedMaxStateMonitorVariable'
						]),
					'self.LeakedMaxSpikeMonitorVariable.t is '+str(
							self.LeakedMaxSpikeMonitorVariable.t
						)
				]
			)
			'''

			#Check
			if self.LeakingMinPhaseTimeVariable==None:
				self.LeakingMinPhaseTimeVariable=1.*self.BrianedParentNetworkDeriveBrianerVariable.SimulatingStopTimeFloat*self.BrianedParentNetworkDeriveBrianerVariable.BrianedTimeQuantityVariable/2.

			#Check
			#if self.LeakingMaxPhasesInt==None:
			#	#self.LeakingMaxPhasesInt=len(self.LeakedMaxSpikeMonitorVariable.t)
			#	self.LeakingMaxPhasesInt=2

			#debug
			"""
			self.debug(
				[
					('self.',self,[
							'LeakingMinPhaseTimeVariable',
							'LeakingMaxPhasesInt'
						])
				]
			)
			"""

			#init
			self.LeakedPhaseList=[None]*self.LeakingUnitsInt

			#loop
			for __IndexInt,__NeuronInt in enumerate(
				self.LeakedMaxSpikeMonitorVariable.i
			):

				#debug
				'''
				self.debug(
					[
						'[__IndexInt,__NeuronInt] is '+str(
							[__IndexInt,__NeuronInt]
						)
					]
				)
				'''

				#get
				LeakedTimeVariable=self.LeakedMaxSpikeMonitorVariable.t[__IndexInt]

				#Check
				if LeakedTimeVariable>self.LeakingMinPhaseTimeVariable:

					#init
					if self.LeakedPhaseList[__NeuronInt]==None:
						
						#init
						self.LeakedPhaseList[__NeuronInt]=[]

					#init
					LeakedAppendList=[
						__IndexInt,
						float(LeakedTimeVariable),
						None
					]

					#len
					LeakedLenghtInt=len(self.LeakedPhaseList[__NeuronInt])

					#Check
					if LeakedLenghtInt>0 and LeakedLenghtInt<self.LeakingMaxPhasesInt:

						#debug
						'''
						self.debug(
							[
								'We scan the phase with the others'
							]
						)
						'''

						#import
						#import brian2

						#map
						LeakedAppendList[-1]=map(	
							lambda __OtherIndexInt:
							[
								int(self.LeakedMaxSpikeMonitorVariable.i[__OtherIndexInt]),
								float(
				LeakedTimeVariable-self.LeakedMaxSpikeMonitorVariable.t[__OtherIndexInt]
									)
							],
							xrange(
								self.LeakedPhaseList[__NeuronInt][-1][0]+1,
								__IndexInt
							)
						)

						#debug
						'''
						self.debug(
							[
								'LeakedAppendList is '+str(LeakedAppendList)
							]
						)	
						'''

					#Check
					if LeakedLenghtInt<self.LeakingMaxPhasesInt:

						#append
						self.LeakedPhaseList[__NeuronInt].append(LeakedAppendList)

			#debug
			"""
			self.debug(
				[
					'In the end',
					('self.',self,[
							'LeakedPhaseList'
						])
				]
			)
			"""

			"""
			LeakedPhaseList

			[
				neuronIndexInt [
					timeIndexInt,timeFloat,[(neuronIndexInt,timeFloat),...,()]
				]
			]
			"""

			#map
			map(
				lambda __InteractionLeaker:
				__InteractionLeaker.setPhaseWeightArray(),
				self.TeamDict['Interactions'].ManagementDict.values()
			)

			#for __ConnectionLeaker in self['/-Connections'].ManagementDict.items()


			"""
			LeakingWeightVariable=

			#map
			map(
					lambda __NeuronIndexInt,__LeakedPhaseVariable :
					map(
						lambda 
						__ConnectionLeaker.LeakingW __LeakedPhaseVariable[1][0]
					),
					xrange(len(LeakedPhaseList)),
					LeakedPhaseList
				)
			"""

	def simulateEvent(self):

		#BaseClass
		BaseClass.simulateEvent(self)

		#Check
		if self.BrianedParentPopulationDeriveBrianerVariable.LeakingAutoCorrelationBool:

			#debug
			self.debug(
				[
					"We compute autocorrelation"
				]
			)

			#import
			import brian2
			import numpy as np
			
			#set
			BrianedTotalArray=self.BrianedSpikeMonitorVariable.t/brian2.ms
			BrianedWidthFloat=20.;
			BrianedBinFloat=0.5;
			self.LeakedAutoTimeArray=np.arange(
				-BrianedWidthFloat,
				BrianedWidthFloat,
				BrianedBinFloat
			);

			#corre
			self.LeakedGlobalAutoValueArray = correlogram(
				BrianedTotalArray,
				BrianedTotalArray,
				width=BrianedWidthFloat,#*brian2.ms,
				bin=BrianedBinFloat,#*brian2.ms,
			)

			#map
			self.LeakedAutoValueArraysArray = map(
				lambda __FirstInt:
				correlogram(
					self.BrianedSpikesListsList[__FirstInt]/brian2.ms,
					self.BrianedSpikesListsList[__FirstInt]/brian2.ms,
					width=BrianedWidthFloat,#*brian2.ms,
					bin=BrianedBinFloat,#*brian2.ms,
				),
				xrange(len(self.BrianedSpikesListsList))
			)

			#mean
			self.LeakedMeanAutoValueArray=np.mean(self.LeakedAutoValueArraysArray)
			self.LeakedStdAutoValueArray=np.sd(self.LeakedAutoValueArraysArray)

			#debug
			self.debug(
				[
					('self.',self,[
							'LeakedAutoTimeArray',
							'LeakedAutoValueArray'
						])
					#'self.LeakedAutoValueArraysArray is '+str(self.LeakedAutoValueArraysArray)
				]
			)

	def setPhaseWeightArray(self):

		#set
		LeakedPhaseList = self.LeakedParentPopulationDeriveLeakerVariable.LeakedPhaseList
		LeakedBrianWeightFloatsArray = self.LeakedBrianWeightFloatsArray

		#debug
		'''
		self.debug([
				"We set weight versus phase here",
				('self.',self,[
						"LeakedBrianWeightFloatsArray"
					]),
				"LeakedPhaseList is ",str(LeakedPhaseList)
			]
		)
		'''

		#map
		LeakedPeriodTimeFloatsList = map(
			lambda __LeakedPostPhaseVariable:
			__LeakedPostPhaseVariable[1][1]-__LeakedPostPhaseVariable[0][1]
			if __LeakedPostPhaseVariable!=None and len(__LeakedPostPhaseVariable)>1
			else None,
			LeakedPhaseList
		)  

		#debug
		'''
		self.debug(
			[
				"LeakedPeriodTimeFloatsList is "+str(LeakedPeriodTimeFloatsList)
			]
		)
		'''

		#map
		self.LeakedWeightPhaseList = SYS.filterNone(
			map(
				lambda __NeuronIndexInt,__LeakedPostPhaseVariable,__LeakedPeriodTimeFloat :
				map(
					lambda __LeakedPrePhaseVariable:
					(
						LeakedBrianWeightFloatsArray[
							__LeakedPrePhaseVariable[0],
							__NeuronIndexInt
						],
						((
							(__LeakedPrePhaseVariable[1])/__LeakedPeriodTimeFloat
						)-0.5)*360.
						#__LeakedPrePhaseVariable[1]
					)
					if len(__LeakedPostPhaseVariable)>1
					else None,
					__LeakedPostPhaseVariable[1][2]
				)
				if __LeakedPeriodTimeFloat!=None
				else None,
				xrange(len(LeakedPhaseList)),
				LeakedPhaseList,
				LeakedPeriodTimeFloatsList
			)
		)
	
		#debug
		'''
		self.debug(
			[
				"We setted the weight versus the leak",
				('self.',self,[
						'LeakedWeightPhaseList'
					])
			]
		)
		'''

	#/######################/#
	# Augment view
	#

	def viewSample(self):

		#debug
		'''
		self.debug(
			[
				'We leak view sample here',
				('self.',self,[
						'StructureTagStr',
						'ManagementTagStr'
					])
			]
		)
		'''

		#Check
		if self.ParentGrandManagementTagStr!=Recorder.RecordPrefixStr+"J":
			self.ViewingXScaleFloat=1000.
			self.ViewingYScaleFloat=1000.

		#base
		BaseClass.viewSample(self)

	def viewPopulation(self):

		#/##################/#
		# Call all the view input methods
		#

		#debug
		'''
		self.debug(
			[
				'We have to resort the inputs first',
				str(self.TeamDict['Traces'].ManagementDict.keys()),
				('self.',self,[
					'LeakedInputKeyStrsList',
					'LeakedRecordSkipStrsList'
				])
			]
		)
		'''

		#get
		LeakedRunPopulationChartsDerivePyploter=self.getTeamer(
				"Panels"
			).getManager(
				"Run"
			).getTeamer(
				'Charts'
			)

		if self.LeakedInputKeyStrsList==None:
			#/##################/#
			# base method
			#

			#base
			BaseClass.viewPopulation(self)
			return

		#filter
		LeakedInputKeyStrsList=SYS._filter(
					lambda __KeyStr:
					__KeyStr.split(
						Recorder.RecordPrefixStr
					)[1] not in self.LeakedRecordSkipStrsList,
					self.LeakedInputKeyStrsList
				) if len(Recorder.RecordPrefixStr)>0 else SYS._filter(
					lambda __KeyStr:
					__KeyStr not in self.LeakedRecordSkipStrsList,
					self.LeakedInputKeyStrsList
				)

		#map
		map(
			lambda __LeakedInputKeyStr:
			LeakedRunPopulationChartsDerivePyploter.getManager(
				__LeakedInputKeyStr
			),
			LeakedInputKeyStrsList
		)


		#/##################/#
		# Do we plot spike correlation
		#

		#Check
		if self.LeakingAutoCorrelationBool:

			#debug
			self.debug(
				[
					'we plot autocorrelation here'
				]
			)

			#get
			LeakedAutoPopulationChartDerivePyploter=self.getTeamer(
					"Panels"
				).getManager(
					"Stat"
				).getTeamer(
					'Charts'
				).getManager(
					'Auto'
				).getTeamer(
					'Draws'
				).getManager(
					'0'
				)

			LeakedAutoPopulationChartDerivePyploter.PyplotingDrawVariable=map(
				lambda __EventVariable:
				(
					'plot',
					{
							'#liarg':[
								__EventVariable.LeakedAutoTimeArray,
								__EventVariable.LeakedAutoValueArray
							],
							'#kwarg':dict(
								{
									'linestyle':'-',
									'linewidth':3
								}
							)
					}	
				),
				self.TeamDict['Events'].ManagementDict.values()
			)

			LeakedAutoNetworkChartDerivePyploter=self.BrianedParentNetworkDeriveBrianerVariable.getTeamer(
					"Panels"
				).getManager(
					"Stat"
				).getTeamer(
					'Charts'
				).getManager(
					self.ManagementTagStr+'_Auto'
				).getTeamer(
					'Draws'
				).getManager(
					'0'
				)
			LeakedAutoNetworkChartDerivePyploter.PyplotingDrawVariable = LeakedAutoPopulationChartDerivePyploter.PyplotingDrawVariable

		#/##################/#
		# base method
		#

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
		
		#init
		ViewedRunNetworkDrawsDerivePyploter=None
		
		#get
		ViewedRunPopulationDrawsDerivePyploter=LeakedRunPopulationChartsDerivePyploter.getManager(
				Recorder.RecordPrefixStr+self.LeakedSymbolStr
			).getTeamer(
				'Draws'
			)

		#Check
		if len(ViewedRunPopulationDrawsDerivePyploter.ManagementDict)>0:

			#debug
			"""
			self.debug(
				[
					"Are we going to plot global traces ?",
					('self.',self,['LeakingGlobalBool','LeakingTotalBool'])
				]
			)
			"""

			#Check
			if self.LeakingGlobalBool or self.LeakingTotalBool:

				#/##################/#
				# view at the population scale
				#

				#Check
				if self.LeakingTotalBool:

					#alias
					ViewedMeanFloatsArray=self.NumscipiedMeanGlobalFloatsArray

					#alias
					ViewedHalfStdFloatsArray=self.NumscipiedStdGlobalFloatsArray

				else:

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
					ViewedHalfStdFloatsArray=np.sqrt(
						getattr(
							self.LeakedVarStateMonitorVariable,
							'Var_'+self.LeakedSymbolStr
						)[0,:]
					)


				#divide
				ViewedHalfStdFloatsArray/=2.

				#Check
				ViewedMaxStdFloatsArray=ViewedMeanFloatsArray+ViewedHalfStdFloatsArray
				ViewedMinStdFloatsArray=ViewedMeanFloatsArray-ViewedHalfStdFloatsArray
				

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
				
				#add
				ViewedRunPopulationDrawsDerivePyploter.getManager(
						'Global'
					).PyplotingDrawVariable=[
						(	
							'plot',
							{
								'#liarg':[
									self.LeakedSimulationStateMonitorVariable.t,
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
									self.LeakedSimulationStateMonitorVariable.t,
									ViewedMaxStdFloatsArray
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
									self.LeakedSimulationStateMonitorVariable.t,
									ViewedMinStdFloatsArray
									
								],
								'#kwarg':dict(
									{
										'linestyle':'--',
										'linewidth':1,
										'color':'black',
									}
								)
							}	
						),
						(
							'fill_between',
							{
								'#liarg':[
									self.LeakedSimulationStateMonitorVariable.t,
									ViewedMinStdFloatsArray,
									ViewedMaxStdFloatsArray
								],
								'#kwarg':dict(
									{
										'color':'black',
										'alpha':0.2
									}
								)
							}
						)
					]

				#/##################/#
				# view at the network scale
				#

				#alias
				ViewedRunNetworkDrawsDerivePyploter=self.BrianedParentNetworkDeriveBrianerVariable.getTeamer(
					'Panels'
				).getManager(
					'Run'
				).getTeamer(
					'Charts'
				).getManager(
					self.ManagementTagStr+'_'+Recorder.RecordPrefixStr+self.LeakedSymbolStr
				).getTeamer(
					'Draws'
				)

				#get
				ViewedRunNetworkDrawsDerivePyploter.getManager(
						'Global'
					).PyplotingDrawVariable=ViewedRunPopulationDrawsDerivePyploter.ManagementDict[
						'Global'
					].PyplotingDrawVariable

				#/##################/#
				# add a stat view
				#

				"""

				#get
				ViewedStatDerivePyploter=self.BrianedParentNetworkDeriveBrianerVariable.getTeamer(
					'Panels'
				).getManager(
					'Stat'
				)

				#get
				ViewedStatDerivePyploter.getTeamer(
					'Charts'
				).getManager(
					'Correlation'
				).getTeamer(
					'Draws'
				).getManager(
					'Global'
				).PyplotingDrawVariable=[
					(	
						'plot',
						{
							'#liarg':[
								self.LeakedAutocorrelationGlobalFloatsArray
								
							],
							'#kwarg':dict(
								{
									'linestyle':'-',
									'linewidth':2,
									'color':'black',
								}
							)
						}	
					)
				]
				"""

			#Check
			if self.LeakingMaxBool:

				#/################/#
				# Max in the traces
				#

				#debug
				"""
				self.debug(
					[
						"We are going to plot the maximums time",
						('self.',self,['LeakedMaxStateMonitorVariable'])
					]
				)
				"""

				#add
				"""
				ViewedRunPopulationDrawsDerivePyploter.getManager(
						'Max'
					).PyplotingDrawVariable=map(
						lambda 
						(	
							'plot',
							{
								'#liarg':[
									self.LeakedMaxStateMonitorVariable.t,
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
						self.LeakedMaxStateMonitorVariable.t
					)
				"""


				#/################/#
				# Phase versus weights
				#

				#debug
				"""
				self.debug(
					[
						'We build a view of the phase compared to J',
						('self.',self,['LeakedPhaseList'])
					]
				)
				"""

				#map
				map(
					lambda __InteractionLeaker:
					__InteractionLeaker.plotPhaseWeight(),
					self.TeamDict['Interactions'].ManagementDict.values()
				)


	def plotCorrelogramm(self):

		#debug
		'''
		self.debug(
			[
				"We plot the spike correlogramm",
				('self.',self,[
						"LeakedWeightPhaseList"
					])
			]
		)
		'''

		#set
		ChartStr=str(self.ManagementTagStr)+"_Correlogramm"

		#add
		LeakedPhaseWeightPopulationChartDerivePyploter = self.LeakedParentPopulationDeriveLeakerVariable.getTeamer(
			"Panels"
		).getManager(
			"Stat"
		).getTeamer(
			"Charts"
		).getManager(
			ChartStr
		)


	def plotPhaseWeight(self):

		#debug
		'''
		self.debug(
			[
				"We plot the phase and the weights",
				('self.',self,[
						"LeakedWeightPhaseList"
					])
			]
		)
		'''

		#set
		ChartStr=str(self.ManagementTagStr)+"_PhaseWeight"

		#add
		LeakedPhaseWeightPopulationChartDerivePyploter = self.LeakedParentPopulationDeriveLeakerVariable.getTeamer(
			"Panels"
		).getManager(
			"Stat"
		).getTeamer(
			"Charts"
		).getManager(
			ChartStr
		)

		LeakedPhaseWeightPopulationDrawDerivePyploter = LeakedPhaseWeightPopulationChartDerivePyploter.getTeamer(
			"Draws"
		).getManager(
			"0"
		)

		#flat
		LeakedFlatWeightPhaseList=SYS.sum(self.LeakedWeightPhaseList)

		#debug
		'''
		self.debug(
			"LeakedFlatWeightPhaseList is "+SYS._str(LeakedFlatWeightPhaseList)
		)
		'''
		
		#debug
		[
			LeakedWeightFloatsArray,
			LeakedPhaseFloatsArray
		]=SYS.unzip(
			LeakedFlatWeightPhaseList,
			[0,1],
			_ArrayBool=True
		)

		#debug
		'''
		self.debug(
			[
				"LeakedWeightFloatsArray is ",str(LeakedWeightFloatsArray),
				"LeakedPhaseFloatsArray is ",str(LeakedPhaseFloatsArray),
			]
		)
		'''

		#/##################/#
		# Think already on the max
		#

		#concatenate
		MaxWeightFloat=max(-LeakedWeightFloatsArray.min(),LeakedWeightFloatsArray.max())
		MaxPhaseFloat=max(-LeakedPhaseFloatsArray.min(),LeakedPhaseFloatsArray.max())
		ViewedXLimFloatsArray=[-MaxWeightFloat,MaxWeightFloat]
		ViewedYLimFloatsArray=[-MaxPhaseFloat,MaxPhaseFloat]

		#view
		LeakedPhaseWeightPopulationChartDerivePyploter.view(
			_XLabelStr="$ Weights $",
			_YLabelStr="$ Phases\ (ms) $",
			_XVariable=ViewedXLimFloatsArray,
			_YVariable=ViewedYLimFloatsArray
		)

		#set
		LeakedPhaseWeightPopulationDrawDerivePyploter.PyplotingDrawVariable=map(
						lambda __LeakedWeightPhaseVariable:
						(	
							'plot',
							{
								'#liarg':SYS.unzip(
									__LeakedWeightPhaseVariable,
									[0,1],
									_ArrayBool=True
								),
								'#kwarg':dict(
									{
										'linestyle':'',
										'marker':"o",
										'markersize':3.
									}
								)
							}	
						),
						self.LeakedWeightPhaseList[:2]
					)+[

						(	
							'plot',
							{
								'#liarg':[
									ViewedXLimFloatsArray,
									[0,0]
								],
								'#kwarg':dict(
									{
										'linestyle':'--',
										'color':'black'
									}
								)
							}	
						),
						(	
							'plot',
							{
								'#liarg':[
									[0,0],
									ViewedYLimFloatsArray
									
								],
								'#kwarg':dict(
									{
										'linestyle':'--',
										'color':'black'
									}
								)
							}	
						)
					]

		#set
		BrianedParentNetworkChartDeriveBrianerVariable = self.LeakedParentNetworkDeriveLeakerVariable.getTeamer(
			"Panels"
		).getManager(
			"Stat"
		).getTeamer(
			"Charts"
		).getManager(
			ChartStr
		)

		#view
		BrianedParentNetworkChartDeriveBrianerVariable.view(
			_XLabelStr="$ Weights $",
			_YLabelStr="$ Phases\ (ms) $",
			_XVariable=ViewedXLimFloatsArray,
			_YVariable=ViewedYLimFloatsArray
		)

		#set
		BrianedParentNetworkDrawDeriveBrianerVariable=BrianedParentNetworkChartDeriveBrianerVariable.getTeamer(
			"Draws"
		).getManager(
			"0"
		).PyplotingDrawVariable = LeakedPhaseWeightPopulationDrawDerivePyploter.PyplotingDrawVariable


	def viewInteraction(self):

		#Check
		if self.LeakingEigenBool:


			#debug
			'''
			self.debug(
				[
					'We want to see the eigen of the connectivity',
					('self.',self,[
							'NumscipiedRealEigenvalueFloatsArray'
						])
				]
			)
			'''

			#/##################/#
			# Build the theoritical ellipse
			#

			#import
			import matplotlib.patches

			#Add the matrix contour Ellipse
			PyplotedBifurcationEllipse=matplotlib.patches.Ellipse(
								xy=(self.NumscipiedCenterFloat,0.), 
							 	width=self.NumscipiedWidthFloat,
							 	height=self.NumscipiedHeightFloat,
							 	color='r',
						)
			PyplotedBifurcationEllipse.set_alpha(0.2)

			#Add the Wiener Circle
			PyplotedBifurcationCircle=matplotlib.patches.Ellipse(
								xy=(self.NumscipiedCenterFloat,0.), 
							 	width=2.,
							 	height=2.,
							 	linewidth=2,
							 	color='black',
							 	fill=False
						)
			PyplotedBifurcationCircle.set_alpha(0.4)

			#/##################/#
			# draw
			#

			#debug
			'''
			self.debug(
				[
					'We draw',
					('self.',self,[
							'PyplotingDrawVariable'
						])
				]
			)
			'''

			#list
			self.PyplotingDrawVariable=[
				(
					'plot',
					{
						'#liarg':[
							[-2.,2.],
							[0.,0.]
						],
						'#kwarg':dict(
							{
								'linestyle':"--",
								'linewidth':1,
								'color':'black'
							}
						)
					}
				),
				(
					'plot',
					{
						'#liarg':[
							[-0.,0.],
							[-2.,2.]
						],
						'#kwarg':dict(
							{
								'linestyle':"--",
								'linewidth':1,
								'color':'black'
							}
						)
					}
				),
				(
					'plot',
					{
						'#liarg':[
							[1.,1.],
							[-2.,2.]
						],
						'#kwarg':dict(
							{
								'linestyle':"-",
								'linewidth':2,
								'color':'black',
								'alpha':0.5
							}
						)
					}
				),
				(
					'add_artist',
					PyplotedBifurcationEllipse
				),
				(
					'add_artist',
					PyplotedBifurcationCircle
				),
				(
					'plot',
					{
						'#liarg':[
							self.NumscipiedRealEigenvalueFloatsArray,
							self.NumscipiedImagEigenvalueFloatsArray
						],
						'#kwarg':dict(
							{
								'linestyle':"",
								'marker':'o',
								'color':'black'
							}
						)
					}
				)
			]
			
			#/##################/#
			# View chart
			#

			#import
			import numpy as np

			#concatenate
			ViewedVariablesArray=np.concatenate(
				[
					self.NumscipiedRealEigenvalueFloatsArray,
					self.NumscipiedImagEigenvalueFloatsArray
				]
			)
			ViewedMinFloat=ViewedVariablesArray.min()
			ViewedMaxFloat=max(ViewedVariablesArray.max(),1.)
			ViewedLimFloatsArray=[ViewedMinFloat,ViewedMaxFloat]


			#/##################/#
			# set at the level of the network
			#


			#get
			ViewedConnectivityChartDerivePyploter=self.LeakedParentNetworkDeriveLeakerVariable.getTeamer(
				'Panels'
			).getManager(
				'Eigen',
				_IndexInt=0
			).getTeamer(
				'Charts'
			).getManager(
				'Connectivity'
			)

			#alias
			ViewedConnectivityChartDerivePyploter.PyplotingDrawVariable=self.PyplotingDrawVariable

			#view
			ViewedConnectivityChartDerivePyploter.view(
				_XLabelStr="$Re(\lambda_{J})$",
				_YLabelStr="$Im(\lambda_{J})$",
				_XVariable=ViewedLimFloatsArray,
				_YVariable=ViewedLimFloatsArray
			)

		#call the base method
		BaseClass.viewInteraction(self)


	#/###################/#
	# Other methods
	#

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

			#add
			self.LeakedParentPopulationDeriveLeakerVariable.LeakedModelStr+=self.LeakedSymbolStr+'='+self.LeakedEquationStr+' : '+self.LeakedParentPopulationDeriveLeakerVariable.LeakedDimensionStr+"\n"
		
		elif self.LeakedClampStr in ['Custom','Network']:

			#debug
			'''
			self.debug(
				[
					'We set Operation',
					('self.',self,[
							'LeakedSymbolStr'
						])
				]
			)
			'''

			#add
			self.LeakedParentPopulationDeriveLeakerVariable.LeakedModelStr+=self.LeakedSymbolStr+' : '+self.LeakedParentPopulationDeriveLeakerVariable.LeakedDimensionStr+"\n"

		#add in the current
		self.LeakedParentPopulationDeriveLeakerVariable.addCurrentStr(
			self.LeakedSymbolStr
		)

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
					[
						'LeakedModelStr'
					],
					'LeakerClass'
				)

		#/##################/#
		# Call the base method
		#

		#call
		BaseClass._print(self,**_KwargVariablesDict)

	def filterSpikespace(self):

		#get
		#SpikespaceArray=self.BrianedNeurongroupVariable.variables[
		#	'_spikespace'
		#].get_value()
		Spikespace=self.BrianedNeurongroupVariable._spikespace

		#get
		SpikesInt = Spikespace[-1]

		#debug
		'''
		self.debug(
			[
				'We filterSpikespace here',
				'SpikesInt is '+str(SpikesInt),
				#('self.',self,[
				#		'BrianedNeurongroupVariable'
				#	])
			]
		)
		'''

		#Check
		if SpikesInt > 0:

			#get
			RandomInt = self.LeakedRandomFunction(SpikesInt)

			#Set the first spike
			Spikespace[0] = Spikespace[
				:SpikesInt
			][
				RandomInt
			]

			# Set the total number of spikes to 1
			Spikespace[-1]=1

			#debug
			'''
			self.debug(
				[
					'We have chosen the '+str(RandomInt)+' index to spike',
					'Spikespace is '+str(Spikespace)
				]
			)	
			'''

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
		'BrianingMonitorIndexIntsList',
		'LeakingTimeUnitStr',
		'LeakingInteractionStr',
		'LeakingSymbolPrefixStr',
		'LeakingWeightVariable',
		'LeakingTransferVariable',
		'LeakingThresholdVariable',
		'LeakingResetVariable',
		'LeakingRefractoryVariable',
		'LeakingVariableStr',
		'LeakingRecordBool',
		'LeakingNoiseStdVariable',
		'LeakingDelayVariable',
		'LeakingDelayCustomBool',
		'LeakingDelayPrepostBool',
		'LeakingPlasticRuleVariable',
		'LeakingPlasticPreBool',
		'LeakingGlobalBool',
		'LeakingTotalBool',
		'LeakingThresholdMethodStr',
		'LeakingEigenBool',
		'LeakingMaxBool',
		'LeakingMinPhaseTimeVariable',
		'LeakingMaxPhasesInt',
		'LeakingAutoCorrelationBool',
		'LeakedStepTimeFloat',
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
		'LeakedInteractionWeightFloat',
		'LeakedParentSingularStr',
		'LeakedParentNetworkDeriveLeakerVariable',
		'LeakedParentPopulationDeriveLeakerVariable',
		'LeakedParentInteractomeDeriveLeakerVariable',
		'LeakedTimedArrayVariable',
		'LeakedVariableStr',
		'LeakedDelayTimeFloatsArray',
		'LeakedDelayTotalIntVariable',
		'LeakedDelayValueFloatVariable',
		'LeakedDelayCursorIntVariable',
		'LeakedDelayActivityFloatsArray',
		'LeakedDelayBufferFloatsArray',
		'LeakedDelaySymbolStr',
		'LeakedMinFloat',
		'LeakedMaxFloat',
		'LeakedMeanGlobalFloatsArray',
		'LeakedStdGlobalFloatsArray',
		'LeakedSimulationStateMonitorVariable',
		'LeakedThresholdMethod',
		'LeakedRandomFunction',
		'LeakedInputKeyStrsList',
		'LeakedBrianWeightFloatsArray',
		'LeakedMeanStateMonitorVariable',
		'LeakedVarStateMonitorVariable',
		'LeakedMaxSpikeMonitorVariable',
		'LeakedMaxStateMonitorVariable',
		'LeakedGlobalSynapsesVariable',
		'LeakedPhaseList',
		'LeakedWeightPhaseList'
	]
)
#<DefinePrint>
