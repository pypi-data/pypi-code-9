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
BaseModuleStr="ShareYourSystem.Standards.Controllers.Systemer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
SYS.addDo('Predicter','Predict','Predicting','Predicted')
#</DefineAugmentation>

#<ImportSpecificModules>
import scipy.stats
import numpy as np
from matplotlib import pyplot
#</ImportSpecificModules>

#<DefineLocals>
def getNullFloatsArray(_FloatsArray, _RtolFloat=1e-5):
	u, s, v = np.linalg.svd(_FloatsArray)
	RankInt = (s > _RtolFloat*s[0]).sum()
	return v[RankInt:].T.copy()
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class PredicterClass(BaseClass):
	
	def default_init(self,

						_PredictingUnitsInt=0,
						_PredictingSensorsInt=0,

						_PredictingConstantTimeFloat=0.01,
						_PredictingDecoderWeigtFloat=1.,
						_PredictingNormalisationInt=1,			

						_PredictingCostFloat=1.,
						_PredictingPerturbativeInputWeightFloat=0.1,
						_PredictingPerturbativeLateralWeightFloat=0.1,
						_PredictingInputStatStr='norm',
						_PredictingInputRandomStatStr='norm',
						_PredictingLateralRandomStatStr='norm',

						_PredictedSensorJacobianFloatsArray=None,
						
						_PredictedControlDecoderWeigthFloatsArray=None,
						_PredictedExactDecoderWeigthFloatsArray=None,

						_PredictedLeakWeigthFloatsArray=None,

						_PredictedInputRandomFloatsArray=None,
						_PredictedPerturbativeInputWeigthFloatsArray=None,
						_PredictedNullFloatsArray=None,
						_PredictedTotalPerturbativeInputWeigthFloatsArray=None,
						
						_PredictedExactLateralWeigthFloatsArray=None,
						_PredictedLeakExactLateralWeigthFloatsArray=None,
						_PredictedLateralRandomFloatsArray=None,
						_PredictedPerturbativeLateralWeigthFloatsArray=None,
						_PredictedTotalPerturbativeLateralWeigthFloatsArray=None,
					
						**_KwargVariablesDict
					):
		""" """		

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_predict(self):

		#/#################/#
		# Sensor care : Prepare the input weigth and the null matrix
		#

		self.PredictedSensorJacobianFloatsArray=-np.diag(
			(1./self.PredictingConstantTimeFloat)*np.ones(
				self.PredictingSensorsInt
			)
		)

		#debug
		'''
		self.debug(
			[
				'We have prepared the sensor jacobian',
				('self.',self,['PredictedSensorJacobianFloatsArray'])
			]
		)
		'''

		#/#################/#
		# Prepare the Decoders weigths
		#

		#Perturbative and exact 

		#random
		self.PredictedExactDecoderWeigthFloatsArray=self.PredictingDecoderWeigtFloat*getattr(
			scipy.stats,
			self.PredictingInputRandomStatStr
		).rvs(
			size=(
				self.PredictingSensorsInt,
				self.PredictingUnitsInt
			)
		)/(self.PredictingUnitsInt**self.PredictingNormalisationInt)
		
		#find the null space
		self.PredictedNullFloatsArray=getNullFloatsArray(
			self.PredictedExactDecoderWeigthFloatsArray
		)

		#debug
		'''
		PredictedProductArray=np.dot(
			self.PredictedExactDecoderWeigthFloatsArray,
			self.PredictedNullFloatsArray
		)
		self.debug(
				[
					('self.',self,[
						'PredictedExactDecoderWeigthFloatsArray',
						'PredictingUnitsInt'
						]
					),
					("locals()['",locals(),['PredictedProductArray'],"']")
				]
			)
		'''

		#Control 

		#pinv
		self.PredictedControlDecoderWeigthFloatsArray=np.linalg.pinv(
				self.PredictedExactDecoderWeigthFloatsArray.T
			)

		#debug
		'''
		PredictedPinvFloatsArray=np.dot(
			self.PredictedControlDecoderWeigthFloatsArray,
			self.PredictedExactDecoderWeigthFloatsArray.T
		)
		self.debug(
			[
				'PredictedPinvFloatsArray is ',
				str(PredictedPinvFloatsArray)
			]
		)
		'''

		#/#################/#
		# Build the perturbative random matrices
		#

		#random
		self.PredictedInputRandomFloatsArray=self.PredictingPerturbativeInputWeightFloat*getattr(
			scipy.stats,
			self.PredictingInputRandomStatStr
		).rvs(
			size=(
				np.shape(self.PredictedNullFloatsArray)[1],
				self.PredictingSensorsInt
			)
		)

		#dot
		self.PredictedPerturbativeInputWeigthFloatsArray=np.dot(
				self.PredictedNullFloatsArray,
				self.PredictedInputRandomFloatsArray
			)

		#/#################/#
		# Build all the perturbative input
		#

		#sum
		self.PredictedTotalPerturbativeInputWeigthFloatsArray=self.PredictedExactDecoderWeigthFloatsArray.T+self.PredictedPerturbativeInputWeigthFloatsArray

		#/#################/#
		# Build all the perturbative input
		#

		self.PredictedLeakWeigthFloatsArray=np.diag(np.ones(self.PredictingUnitsInt))

		#/#################/#
		# Build all the possible lateral connectivities
		#

		#Exact

		#dot
		self.PredictedExactLateralWeigthFloatsArray=np.dot(
				self.PredictedExactDecoderWeigthFloatsArray.T,
				self.PredictedExactDecoderWeigthFloatsArray
			)

		#add the leaky part to compensate
		self.PredictedLeakExactLateralWeigthFloatsArray=self.PredictedExactLateralWeigthFloatsArray-(
			1.-self.PredictingCostFloat)*np.diag(
			np.ones(self.PredictingUnitsInt)
		)

		#Perturbative

		#random
		self.PredictedLateralRandomFloatsArray=self.PredictingPerturbativeLateralWeightFloat*getattr(
			scipy.stats,
			self.PredictingLateralRandomStatStr
		).rvs(
			size=(
				np.shape(self.PredictedNullFloatsArray)[1],
				self.PredictingUnitsInt
			)
		)

		#dot
		self.PredictedPerturbativeLateralWeigthFloatsArray=np.dot(
				self.PredictedNullFloatsArray,
				self.PredictedLateralRandomFloatsArray
			)

		#sum
		self.PredictedTotalPerturbativeLateralWeigthFloatsArray=self.PredictedLeakExactLateralWeigthFloatsArray+self.PredictedPerturbativeLateralWeigthFloatsArray
#</DefineClass>

#</DefinePrint>
PredicterClass.PrintingClassSkipKeyStrsList.extend(
	[
		'PredictingUnitsInt',
		'PredictingSensorsInt',
		
		'PredictingConstantTimeFloat',
		'PredictingDecoderWeigtFloat',
		'PredictingNormalisationInt',

		'PredictingCostFloat',
		'PredictingPerturbativeInputWeightFloat',
		'PredictingPerturbativeLateralWeightFloat',
		'PredictingInputStatStr',
		'PredictingInputRandomStatStr',
		'PredictingLateralRandomStatStr',

		'PredictedSensorJacobianFloatsArray',
		
		'PredictedLeakWeigthFloatsArray',

		'PredictedControlDecoderWeigthFloatsArray',
		'PredictedExactDecoderWeigthFloatsArray',

		'PredictedInputRandomFloatsArray',
		'PredictedPerturbativeInputWeigthFloatsArray',
		'PredictedNullFloatsArray',
		'PredictedTotalPerturbativeInputWeigthFloatsArray',
		
		'PredictedExactLateralWeigthFloatsArray',
		'PredictedLeakExactLateralWeigthFloatsArray',
		'PredictedLateralRandomFloatsArray',
		'PredictedPerturbativeLateralWeigthFloatsArray',
		'PredictedTotalPerturbativeLateralWeigthFloatsArray',
	]
)
#<DefinePrint>