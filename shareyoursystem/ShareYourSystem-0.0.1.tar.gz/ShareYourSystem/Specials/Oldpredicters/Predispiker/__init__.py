# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


"""

#<DefineAugmentation>
import ShareYourSystem as SYS
import types
BaseModuleStr="ShareYourSystem.Specials.Predicters.Predicter"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
SYS.appendDoStrsList(['Predispiker','Predispike','Predispiking','Predispiked'])
#</DefineAugmentation>

#<ImportSpecificModules>
import scipy.stats
import numpy as np
from matplotlib import pyplot
#</ImportSpecificModules>

#<DefineLocals>
def getKrenelFloatsArray(
		_LevelFloatsTuple=None,
		_TimeFloatsTuple=None,
		_RunTimeFloat=0.01,
		_StepTimeFloat=0.0001,
	):

	#get the bins
	BinsInt=_RunTimeFloat/_StepTimeFloat

	#init
	KrenelFloatsArray=_LevelFloatsTuple[0]*np.ones(
		BinsInt,
		dtype=type(_LevelFloatsTuple[0])
	)

	#Debug
	'''
	print('getKrenelFloatsArray')
	print('_TimeFloatsTuple[0]/_StepTimeFloat:_TimeFloatsTuple[1]/_StepTimeFloat')
	print(_TimeFloatsTuple[0]/_StepTimeFloat,_TimeFloatsTuple[1]/_StepTimeFloat)
	print('_LevelFloatsTuple[1] is '+str(_LevelFloatsTuple[1]))
	print('')
	'''

	#put the second level
	KrenelFloatsArray[
		int(_TimeFloatsTuple[0]/_StepTimeFloat):int(_TimeFloatsTuple[1]/_StepTimeFloat)
	]=_LevelFloatsTuple[1]

	#return
	return KrenelFloatsArray

def getThresholdArray(_Variable,_ThresholdFloat=1.):

	#Check
	if type(_Variable) in [np.float64,float,int]:

		#return
		return max(
				min(
					_Variable,
					_ThresholdFloat
					),
				-_ThresholdFloat
			)
	else:

		#return
		return map(
			lambda __ElementVariable:
			getThresholdArray(
				__ElementVariable,
				_ThresholdFloat=_ThresholdFloat
			),
			_Variable
		)
SYS.getThresholdArray=getThresholdArray
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class PredispikerClass(BaseClass):
	
	def default_init(self,

		_PredispikingRestFloat=-60.,
		_PredispikedRestOverTimeFloat=-60./0.01,
		_PredispikedUnitLeakWeigthFloatsArray=None,

		_PredispikedInitialSensorFloatsArray=None,
		_PredispikedInitialRateFloatsArray=None,
		
		_PredispikedSensorTraceFloatsArray=None,
		_PredispikedPerturbativeUnitTraceFloatsArray=None,
		_PredispikedExactUnitTraceFloatsArray=None,
		_PredispikedControlUnitTraceFloatsArray=None,
		
		_PredispikedPerturbativeDecoderTraceFloatsArray=None,
		_PredispikedExactDecoderTraceFloatsArray=None,
		_PredispikedControlDecoderTraceFloatsArray=None,

		**_KwargVariablesDict
	):
		""" """		

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_predispike(self):

		#/#################/#
		# Special spike change for the lateral don't count the leak part
		#

		#sum
		self.PredictedTotalPerturbativeLateralWeigthFloatsArray=self.PredictedExactLateralWeigthFloatsArray+self.PredictedPerturbativeLateralWeigthFloatsArray
		
		#/#################/#
		# Neuron care : Compute rest over time, threshold 
		#

		#rest
		self.PredispikedRestOverTimeFloat=self.PredispikingRestFloat/self.PredictingConstantTimeFloat

		#compute
		self.PredispikingThresholdFloatsArray=self.PredispikingRestFloat+0.5*np.array(
			map(
				lambda __FloatsArray:
				sum(__FloatsArray**2),
				self.PredictedExactDecoderWeigthFloatsArray
			)
		)

		#debug
		self.debug(
				[
					('self.',self,[
						'PredictingConstantTimeFloat',
						'PredispikingRestFloat',
						'PredispikedRestOverTimeFloat',
						'PredispikingThresholdFloatsArray'
						]
					)
				]
			)

		#/#################/#
		# Neuron care : adapt the leak term in neuron
		#

		#multiply
		self.PredispikedUnitLeakWeigthFloatsArray=self.PredictedLeakWeigthFloatsArray/self.PredictingConstantTimeFloat

		

		#/#################/#
		# Prepare the initial conditions
		#

		#random sensors
		PredispikedInitialSensorFloatsArray=0.1*self.PredispikingClampFloat*scipy.stats.uniform.rvs(
			size=self.PredictingSensorsInt
		)
		
		#random units
		PredispikedInitialRateFloatsArray=self.PredispikingRestFloat+scipy.stats.uniform.rvs(
			size=self.PredictingUnitsInt
		)
		
		#debug
		self.debug(
				[
					'PredispikedInitialRateFloatsArray is ',
					str(PredispikedInitialRateFloatsArray)
				]
			)

		#/#################/#
		# Shape the size of all the runs
		#

		#init sensors
		self.PredispikedSensorTraceFloatsArray=np.zeros(
				(self.PredictingSensorsInt,len(self.PredispikedTimeFloatsArray))
			)
		self.PredispikedSensorTraceFloatsArray[:,0]=PredispikedInitialSensorFloatsArray

		#init perturbative rates
		self.PredispikedPerturbativeUnitTraceFloatsArray=np.zeros(
				(self.PredictingUnitsInt,len(self.PredispikedTimeFloatsArray))
			)
		self.PredispikedPerturbativeUnitTraceFloatsArray[:,0]=PredispikedInitialRateFloatsArray

		#init exact rates
		self.PredispikedExactUnitTraceFloatsArray=np.zeros(
				(self.PredictingUnitsInt,len(self.PredispikedTimeFloatsArray))
			)
		self.PredispikedExactUnitTraceFloatsArray[:,0]=PredispikedInitialRateFloatsArray

		#init leak control rates
		self.PredispikedControlUnitTraceFloatsArray=np.zeros(
				(self.PredictingUnitsInt,len(self.PredispikedTimeFloatsArray))
			)
		self.PredispikedControlUnitTraceFloatsArray[:,0]=PredispikedInitialRateFloatsArray

		#init perturbative decoder
		self.PredispikedPerturbativeDecoderTraceFloatsArray=np.zeros(
				(self.PredictingSensorsInt,len(self.PredispikedTimeFloatsArray))
			)
		self.PredispikedPerturbativeDecoderTraceFloatsArray[:,0]=np.dot(
				self.PredictedExactDecoderWeigthFloatsArray,
				PredispikedInitialRateFloatsArray
			)

		#init exact decoder
		self.PredispikedExactDecoderTraceFloatsArray=np.zeros(
				(self.PredictingSensorsInt,len(self.PredispikedTimeFloatsArray))
			)
		self.PredispikedExactDecoderTraceFloatsArray[:,0]=np.dot(
				self.PredictedExactDecoderWeigthFloatsArray,
				PredispikedInitialRateFloatsArray
			)

		#init leak control decoder
		self.PredispikedControlDecoderTraceFloatsArray=np.zeros(
				(self.PredictingSensorsInt,len(self.PredispikedTimeFloatsArray))
			)
		self.PredispikedControlDecoderTraceFloatsArray[:,0]=np.dot(
				self.PredictedControlDecoderWeigthFloatsArray,
				PredispikedInitialRateFloatsArray
			)

		#/#################/#
		# integrativ Loop
		#

		#for loop
		for __IndexInt in xrange(1,len(self.PredispikedTimeFloatsArray)):

			#/#################/#
			# Sensor part
			#

			#debug
			self.debug(
					[
						'shape(self.PredispikedCommandTraceFloatsArray) is '+str(
							np.shape(self.PredispikedCommandTraceFloatsArray)
						),
						'shape(self.PredispikedSensorTraceFloatsArray) is '+str(
							np.shape(self.PredispikedSensorTraceFloatsArray)
						),
						('self.',self,[
							'PredictedSensorJacobianFloatsArray'
						])
					]
				)

			#Current
			PredispikedSensorCurrentFloatsArray=np.dot(
				self.PredictedSensorJacobianFloatsArray,
				self.PredispikedSensorTraceFloatsArray[:,__IndexInt-1]
			)+self.PredispikedCommandTraceFloatsArray[:,__IndexInt-1]

			"""

			#/#################/#
			# Perturbative Voltage
			#

			#debug
			self.debug(
					('self.',self,['PredispikedRestOverTimeFloat'])
				)

			#Init
			PredispikedPerturbativeUnitCurrentFloatsArray=0.

			#Input Current
			PredispikedPerturbativeUnitCurrentFloatsArray+=0.*np.dot(
				self.PredictedTotalPerturbativeInputWeigthFloatsArray,
				self.PredispikedCommandTraceFloatsArray[:,__IndexInt-1]
			)

			#Lateral Current
			PredispikedPerturbativeUnitCurrentFloatsArray-=0.*np.dot(
				self.PredictedTotalPerturbativeLateralWeigthFloatsArray,
				self.PredispikedPerturbativeUnitTraceFloatsArray[:,__IndexInt-1]
			)
			
			#Leak and Cost Current (non transfered)
			PredispikedPerturbativeUnitCurrentFloatsArray-=np.dot(
				self.PredispikedUnitLeakWeigthFloatsArray,
				self.PredispikedPerturbativeUnitTraceFloatsArray[:,__IndexInt-1]
			)-self.PredispikedRestOverTimeFloat

			#/#################/#
			# Exact Voltage
			#

			#Init
			PredispikedExactUnitCurrentFloatsArray=0.

			#Input Current (from the command)
			PredispikedExactUnitCurrentFloatsArray+=0.*np.dot(
				self.PredictedExactDecoderWeigthFloatsArray.T,
				self.PredispikedCommandTraceFloatsArray[:,__IndexInt-1]
			)

			#Lateral Current
			PredispikedExactUnitCurrentFloatsArray-=0.*np.dot(
				self.PredictedExactLateralWeigthFloatsArray,
				self.PredispikedExactUnitTraceFloatsArray[:,__IndexInt-1]
			)

			#Leak Current (non transfered)
			PredispikedExactUnitCurrentFloatsArray-=np.dot(
				self.PredispikedUnitLeakWeigthFloatsArray,
				self.PredispikedExactUnitTraceFloatsArray[:,__IndexInt-1]
			)-self.PredispikedRestOverTimeFloat

			#/#################/#
			# Control Voltage
			#

			#Init
			PredispikedControlUnitCurrentFloatsArray=0

			#Input Current
			PredispikedControlUnitCurrentFloatsArray+=0.*np.dot(
				self.PredictedExactDecoderWeigthFloatsArray.T,
				self.PredispikedCommandTraceFloatsArray[:,__IndexInt-1]
			)

			#Leal Current
			PredispikedControlUnitCurrentFloatsArray-=np.dot(
				self.PredispikedUnitLeakWeigthFloatsArray,
				self.PredispikedControlUnitTraceFloatsArray[:,__IndexInt-1]
			)+self.PredispikedRestOverTimeFloat
			
			"""

			#/#################/#
			# Euler part
			#

			#debug
			self.debug(
					[
						'PredispikedSensorCurrentFloatsArray is ',
						str(PredispikedSensorCurrentFloatsArray)
					]
				)

			#sensor
			self.PredispikedSensorTraceFloatsArray[
				:,
				__IndexInt
			]=self.PredispikedSensorTraceFloatsArray[
				:,
				__IndexInt-1
			]+PredispikedSensorCurrentFloatsArray*self.PredispikingStepTimeFloat

			#debug
			"""
			self.debug(
					[
						'self.PredispikedSensorTraceFloatsArray[:,__IndexInt] is ',
						str(self.PredispikedSensorTraceFloatsArray[:,__IndexInt])
					]
				)
			"""

			"""
			#set
			LocalDict=locals()

			#loop
			for __TagStr in ['Perturbative','Exact','Control']:	

				#set
				getattr(
					self,
					'Predispiked'+__TagStr+'UnitTraceFloatsArray'
				)[:,__IndexInt]=getattr(
							self,
							'Predispiked'+__TagStr+'UnitTraceFloatsArray'
						)[:,__IndexInt-1]+LocalDict[
				'Predispiked'+__TagStr+'UnitCurrentFloatsArray'
				]*self.PredispikingStepTimeFloat
					
			"""

			#/#################/#
			# Post process part
			#

			"""
			#loop
			for __TagStr in ['Perturbative','Exact','Control']:	

				#get
				PredictedVoltageFloatsArray=getattr(
					self,
					'Predispiked'+__TagStr+'UnitTraceFloatsArray'
				)[:,__IndexInt]

				#debug
				'''
				self.debug(
						[
							'PredictedVoltageFloatsArray is ',
							str(PredictedVoltageFloatsArray)
						]
					)
				'''

				#find spike
				PredictedVoltageIndexInt=np.where(
					PredictedVoltageFloatsArray>self.PredispikingThresholdFloatsArray
				)

				#find the corresponding reset
				PredictedResetFloatsArray=np.diag(
					self.PredictedExactLateralWeigthFloatsArray.T
				)[PredictedVoltageIndexInt]

				#debug
				self.debug(
						[
							'Before reset',
							'PredictedVoltageIndexInt is ',
							str(PredictedVoltageIndexInt),
							'PredictedVoltageFloatsArray is ',
							str(PredictedVoltageFloatsArray),
							'PredictedResetFloatsArray is ',
							str(PredictedResetFloatsArray)
						]
					)

				#reset
				PredictedVoltageFloatsArray[
					PredictedVoltageIndexInt
				]-=PredictedResetFloatsArray
				
				#debug
				self.debug(
						[
							'After reset',
							'PredictedVoltageIndexInt is ',
							str(PredictedVoltageIndexInt),
							'PredictedVoltageFloatsArray is ',
							str(PredictedVoltageFloatsArray)
						]
					)
			"""

			"""
			#/#################/#
			# Decoder part
			#

			#dot
			self.PredispikedPerturbativeDecoderTraceFloatsArray[
				:,
				__IndexInt
			]=(
				1.-(
					self.PredispikedPerturbativeDecoderTraceFloatsArray[
					:,__IndexInt-1]/self.PredictingConstantTimeFloat
				)*self.PredispikingStepTimeFloat
			)
			"""

			"""
			+np.dot(
					self.PredictedExactDecoderWeigthFloatsArray[
						:,
						PredictedVoltageIndexInt
					],
					np.ones(len(PredictedVoltageIndexInt))
				)
			"""

			"""
			#exact control
			self.PredispikedExactDecoderTraceFloatsArray[
				:,
				__IndexInt
			]=np.dot(
					self.PredictedExactDecoderWeigthFloatsArray,
					self.PredispikedExactUnitTraceFloatsArray[:,__IndexInt-1]
				)

			#leak control
			self.PredispikedControlDecoderTraceFloatsArray[
				:,
				__IndexInt
			]=np.dot(
					self.PredictedControlDecoderWeigthFloatsArray,
					self.PredispikedControlUnitTraceFloatsArray[:,__IndexInt-1]
				)

			"""

		#/#################/#
		# Plot
		#

		#debug
		self.debug(
			[
				'len(self.PredispikedTimeFloatsArray) is '+str(
					len(self.PredispikedTimeFloatsArray)),
				'np.shape(self.PredispikedCommandTraceFloatsArray) is '+str(
					np.shape(self.PredispikedCommandTraceFloatsArray))
			]
		)

		#init
		pyplot.figure()

		#/#################/#
		# Command and sensors
		#

		#subplot
		PredispikedSensorAxis=pyplot.subplot(3,1,1)

		#command
		map(
				lambda __IndexInt:
				PredispikedSensorAxis.plot(
						self.PredispikedTimeFloatsArray,
						self.PredictingConstantTimeFloat*self.PredispikedCommandTraceFloatsArray[__IndexInt],
						label='$\\tau_{D}c(t)$',
					)
				if __IndexInt<len(self.PredispikedCommandTraceFloatsArray)
				else None,
				[0]
			)

		#debug
		'''
		self.debug(
				('self.',self,['PredispikedSensorTraceFloatsArray'])
			)
		'''

		#sensor
		map(
				lambda __IndexInt:
				PredispikedSensorAxis.plot(
						self.PredispikedTimeFloatsArray,
						self.PredispikedSensorTraceFloatsArray[__IndexInt,:],
						color='g',
						label='$x(t)$',
						linewidth=3
					)
				if __IndexInt<len(self.PredispikedSensorTraceFloatsArray)
				else None,
				[0,1]
			)

		#set
		PredispikedSensorAxis.legend()
		PredispikedSensorAxis.set_ylabel('$\\tau_{D}c(t),\ x(t)$')
		PredispikedSensorAxis.set_xlim([0.,self.PredispikingRunTimeFloat])
		PredispikedSensorAxis.set_ylim(
			[
				-0.1,
				1.5*self.PredispikingClampFloat*self.PredictingConstantTimeFloat
			]
		)

		"""
		#/#################/#
		# neurons
		#

		#subplot
		PredispikedRateAxis=pyplot.subplot(3,1,2)

		#perturbative
		map(
				lambda __IndexInt:
				PredispikedRateAxis.plot(
						self.PredispikedTimeFloatsArray,
						self.PredispikedPerturbativeUnitTraceFloatsArray[__IndexInt,:],
						color='blue',
						linewidth=3
					)
				if __IndexInt<len(self.PredispikedPerturbativeUnitTraceFloatsArray)
				else None,
				[0,1]
			)

		#exact
		map(
				lambda __IndexInt:
				PredispikedRateAxis.plot(
						self.PredispikedTimeFloatsArray,
						self.PredispikedExactUnitTraceFloatsArray[__IndexInt,:],
						color='violet',
						linewidth=2
					)
				if __IndexInt<len(self.PredispikedPerturbativeUnitTraceFloatsArray)
				else None,
				[0,1]
			)

		#leak
		map(
				lambda __IndexInt:
				PredispikedRateAxis.plot(
						self.PredispikedTimeFloatsArray,
						self.PredispikedControlUnitTraceFloatsArray[__IndexInt,:],
						color='brown',
						linewidth=1
					)
				if __IndexInt<len(self.PredispikedControlUnitTraceFloatsArray)
				else None,
				[0,1]
			)

		#set
		PredispikedRateAxis.set_xlim([0.,self.PredispikingRunTimeFloat])
		PredispikedRateAxis.set_ylim(
			[
				max(-80.,self.PredispikedPerturbativeUnitTraceFloatsArray.min()),
				min(10.,self.PredispikedPerturbativeUnitTraceFloatsArray.max())
			]
		)

		#/#################/#
		# decoders
		#

		#subplot
		PredispikedDecoderAxis=pyplot.subplot(3,1,3)

		#sensor
		map(
				lambda __IndexInt:
				PredispikedDecoderAxis.plot(
						self.PredispikedTimeFloatsArray,
						self.PredispikedSensorTraceFloatsArray[__IndexInt],
						color='g',
						linewidth=3
					)
				if __IndexInt<len(self.PredispikedSensorTraceFloatsArray)
				else None,
				[0,1]
			)

		#perturbative
		map(
				lambda __IndexInt:
				PredispikedDecoderAxis.plot(
						self.PredispikedTimeFloatsArray,
						self.PredispikedPerturbativeDecoderTraceFloatsArray[__IndexInt,:],
						color='blue',
						linewidth=3
					)
				if __IndexInt<len(self.PredispikedPerturbativeDecoderTraceFloatsArray)
				else None,
				[0,1]
			)

		#exact
		map(
				lambda __IndexInt:
				PredispikedDecoderAxis.plot(
						self.PredispikedTimeFloatsArray,
						self.PredispikedExactDecoderTraceFloatsArray[__IndexInt,:],
						color='violet',
						linewidth=2
					)
				if __IndexInt<len(self.PredispikedPerturbativeDecoderTraceFloatsArray)
				else None,
				[0,1]
			)

		#leak
		map(
				lambda __IndexInt:
				PredispikedDecoderAxis.plot(
						self.PredispikedTimeFloatsArray,
						self.PredispikedControlDecoderTraceFloatsArray[__IndexInt,:],
						color='brown',
						linewidth=1
					)
				if __IndexInt<len(self.PredispikedControlDecoderTraceFloatsArray)
				else None,
				[0,1]
			)

		#set
		PredispikedDecoderAxis.set_xlim([0.,self.PredispikingRunTimeFloat])
		PredispikedDecoderAxis.set_ylim([-0.1,1.5*self.PredispikingClampFloat])
		"""

		#show
		pyplot.show()

#</DefineClass>

#</DefinePrint>
PredispikerClass.PrintingClassSkipKeyStrsList.extend(
	[
		'PredispikingRunTimeFloat',
		'PredispikingStepTimeFloat',
		'PredispikingClampFloat',
		
		'PredispikedTimeFloatsArray',
		'PredispikedCommandTraceFloatsArray',

		'PredispikingRestFloat',
		'PredispikingRestOverTimeFloat',
		'PredispikedUnitLeakWeigthFloatsArray',

		'PredispikedInitialSensorFloatsArray',
		'PredispikedInitialRateFloatsArray',
		
		'PredispikedSensorTraceFloatsArray',
		'PredispikedPerturbativeUnitTraceFloatsArray',
		'PredispikedExactUnitTraceFloatsArray',
		'PredispikedControlUnitTraceFloatsArray',
		
		'PredispikedPerturbativeDecoderTraceFloatsArray',
		'PredispikedExactDecoderTraceFloatsArray',
		'PredispikedControlDecoderTraceFloatsArray'
	]
)
#<DefinePrint>
